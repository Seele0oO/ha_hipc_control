import logging
import requests
import json
import voluptuous as vol

from homeassistant.components.button import PLATFORM_SCHEMA, ButtonEntity
from homeassistant.const import CONF_MAC, CONF_PHONE, CONF_API_KEY
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PHONE): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.info("Setting up HiPC Reboot Button platform")
    phone = config.get(CONF_PHONE)
    api_key = config.get(CONF_API_KEY)
    mac = config.get(CONF_MAC)
    _LOGGER.info(f"Phone: {phone}, API Key: {api_key}, MAC: {mac}")
    add_entities([HiPCRebootButton(phone, api_key, mac)])

class HiPCRebootButton(ButtonEntity):

    def __init__(self, phone, api_key, mac):
        self._phone = phone
        self._api_key = api_key
        self._mac = mac
        _LOGGER.info("HiPCRebootButton initialized")

    @property
    def name(self):
        return "HiPC Reboot Button"

    def press(self):
        _LOGGER.info("Pressing HiPC Reboot Button")
        self._send_request("2")

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
