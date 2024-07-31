import requests
import json
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import verify_domain_control
import voluptuous as vol

from .const import DOMAIN, CONF_PHONE, CONF_USER_KEY, CONF_MAC

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    phone = entry.data[CONF_PHONE]
    user_key = entry.data[CONF_USER_KEY]
    mac = entry.data[CONF_MAC]

    switch = HiPCSwitch(phone, user_key, mac)
    async_add_entities([switch])

    async def handle_restart_service(call):
        entity_id = call.data.get("entity_id")
        target_switch = next((s for s in hass.data[DOMAIN].values() if s.entity_id == entity_id), None)
        if target_switch:
            target_switch.restart()

    hass.services.async_register(
        DOMAIN, "restart_pc", handle_restart_service,
        schema=vol.Schema({
            vol.Required("entity_id"): cv.entity_id,
        })
    )

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
