import requests
import json
import logging

from homeassistant.components.switch import SwitchEntity

_LOGGER = logging.getLogger(__name__)

CONF_PHONE = "phone"
CONF_USER_KEY = "user_key"
CONF_MAC = "mac"

def setup_platform(hass, config, add_entities, discovery_info=None):
    data = hass.data["hipc_control"]
    phone = data[CONF_PHONE]
    user_key = data[CONF_USER_KEY]
    mac = data[CONF_MAC]

    add_entities([HiPCSwitch(phone, user_key, mac)])

class HiPCSwitch(SwitchEntity):
    def __init__(self, phone, user_key, mac):
        self._phone = phone
        self._user_key = user_key
        self._mac = mac
        self._state = False

    @property
    def name(self):
        return "HiPC Switch"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._send_request("1")
        self._state = True

    def turn_off(self, **kwargs):
        self._send_request("0")
        self._state = False

    def restart(self, **kwargs):
        self._send_request("2")

    def _send_request(self, switch_state):
        url = "https://kjkapi.hipcapi.com/api/openapi/console"
        data = {
            "phone": self._phone,
            "user_key": self._user_key,
            "mac": self._mac,
            "switch": switch_state
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            _LOGGER.info("Request successful: %s", response.text)
        else:
            _LOGGER.error("Request failed: %s", response.text)
