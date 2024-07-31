import logging
import requests
import json
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_MAC, CONF_PHONE, CONF_API_KEY
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SWITCH_SCHEMA = vol.Schema({
    vol.Required(CONF_PHONE): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    phone = config.get(CONF_PHONE)
    api_key = config.get(CONF_API_KEY)
    mac = config.get(CONF_MAC)
    add_entities([HiPCSwitch(phone, api_key, mac)])

class HiPCSwitch(SwitchEntity):

    def __init__(self, phone, api_key, mac):
        self._phone = phone
        self._api_key = api_key
        self._mac = mac
        self._state = False

    @property
    def name(self):
        return "HiPC Power Switch"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._send_request("1")
        self._state = True

    def turn_off(self, **kwargs):
        self._send_request("0")
        self._state = False

    def _send_request(self, switch_state):
        url = "https://kjkapi.hipcapi.com/api/openapi/console"
        data = {
            "phone": self._phone,
            "user_key": self._api_key,
            "mac": self._mac,
            "switch": switch_state
        }
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            _LOGGER.info("Request successful: %s", response.text)
        else:
            _LOGGER.error("Request failed: %s", response.text)
