import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_PHONE, CONF_USER_KEY, CONF_MAC

@callback
def configured_instances(hass):
    return set(entry.data[CONF_PHONE] for entry in hass.config_entries.async_entries(DOMAIN))

class HiPCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="HiPC Control", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_PHONE): str,
                vol.Required(CONF_USER_KEY): str,
                vol.Required(CONF_MAC): str,
            })
        )
