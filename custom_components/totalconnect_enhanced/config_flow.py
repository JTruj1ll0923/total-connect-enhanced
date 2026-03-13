"""Config flow for Total Connect Enhanced."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_USERCODE, DOMAIN

_LOGGER = logging.getLogger(__name__)


class TotalConnectEnhancedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Total Connect Enhanced."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._username: Optional[str] = None
        self._password: Optional[str] = None

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            self._username = user_input[CONF_USERNAME]
            self._password = user_input[CONF_PASSWORD]

            # Test credentials
            try:
                # Import from the local enhanced library
                from .total_connect_client import TotalConnectClient

                client = TotalConnectClient(
                    self._username, 
                    self._password, 
                    {"default": user_input.get(CONF_USERCODE, "1234")}
                )

                if client.is_logged_in():
                    return self.async_create_entry(
                        title="Total Connect Enhanced",
                        data={
                            CONF_USERNAME: self._username,
                            CONF_PASSWORD: self._password,
                            CONF_USERCODE: user_input.get(CONF_USERCODE, "1234"),
                        },
                    )
                else:
                    errors["base"] = "invalid_auth"

            except ImportError:
                _LOGGER.error("Failed to import total_connect_client")
                errors["base"] = "import_error"
            except Exception as err:
                _LOGGER.error(f"Error testing credentials: {err}")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_USERCODE, default="1234"): str,
                }
            ),
            errors=errors,
        )
