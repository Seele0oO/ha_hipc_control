import logging
import requests
import json
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_MAC, CONF_PHONE, CONF_API_KEY
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PHONE): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.info("Setting up HiPC Power Switch platform")
    phone = config.get(CONF_PHONE)
    api_key = config.get(CONF_API_KEY)
    mac = config.get(CONF_MAC)
    _LOGGER.info(f"Phone: {phone}, API Key: {api_key}, MAC: {mac}")
    add_entities([HiPCSwitch(phone, api_key, mac)])

class HiPCSwitch(SwitchEntity):

    def __init__(self, phone, api_key, mac):
        self._phone = phone
        self._api_key = api_key
        self._mac = mac
        self._state = False
        _LOGGER.info("HiPCSwitch initialized")

    @property
    def name(self):
        return "HiPC Power Switch"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        _LOGGER.info("Turning on HiPC Power Switch")
        self._send_request("1")
        self._state = True

    def turn_off(self, **kwargs):
        _LOGGER.info("Turning off HiPC Power Switch")
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
        _LOGGER.info(f"Sending request: {data}")
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:
            _LOGGER.info(f"Request successful: {response.text}")
        else:
            _LOGGER.error(f"Request failed: {response.text}")
