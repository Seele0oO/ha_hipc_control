import logging
import requests
import json
import voluptuous as vol

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_MAC, CONF_API_KEY, CONF_PHONE
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

BUTTON_SCHEMA = vol.Schema({
    vol.Required(CONF_PHONE): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    phone = config[CONF_PHONE]
    api_key = config[CONF_API_KEY]
    mac = config[CONF_MAC]
    add_entities([HiPCRebootButton(phone, api_key, mac)])

class HiPCRebootButton(ButtonEntity):

    def __init__(self, phone, api_key, mac):
        self._phone = phone
        self._api_key = api_key
        self._mac = mac

    @property
    def name(self):
        return "HiPC Reboot Button"

    def press(self):
        self._send_request("2")

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
