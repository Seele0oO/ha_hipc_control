import logging

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    _LOGGER.info("Setting up HiPC Control component")
    return True
