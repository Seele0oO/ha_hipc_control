import requests
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_PHONE, CONF_USER_KEY, CONF_MAC

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    phone = entry.data[CONF_PHONE]
    user_key = entry.data[CONF_USER_KEY]
    mac = entry.data[CONF_MAC]

    async_add_entities([HiPCSwitch(phone, user_key, mac)])

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
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self._send_request("0")
        self._state = False
        self.schedule_update_ha_state()

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
