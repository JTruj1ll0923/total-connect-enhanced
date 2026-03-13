"""Data coordinator for Total Connect Enhanced."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TotalConnectDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Total Connect API."""

    def __init__(self, hass: HomeAssistant, username: str, password: str, usercode: str) -> None:
        """Initialize."""
        self.username = username
        self.password = password
        self.usercode = usercode
        self.client = None
        self._locations = {}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via enhanced library."""
        try:
            # Import the enhanced library
            from . import client as total_connect_client

            def get_client_data():
                if not self.client:
                    self.client = total_connect_client.TotalConnectClient(self.username, self.password, {"default": self.usercode})

                if not self.client.is_logged_in():
                    self.client.login()
                    if not self.client.is_logged_in():
                        raise Exception("Failed to login to Total Connect")

                # Get all location data
                data = {
                    "locations": {},
                    "garage_doors": {},
                    "smart_locks": {},
                }

                for location_id, location in self.client.locations.items():
                    location_data = {
                        "id": location_id,
                        "name": location.location_name,
                        "devices": {},
                    }

                    # Get garage doors using enhanced library
                    try:
                        garage_doors = location.get_garage_doors()
                        data["garage_doors"][location_id] = garage_doors
                        location_data["garage_doors"] = garage_doors
                        _LOGGER.info(f"Found {len(garage_doors)} garage doors for location {location_id}")
                    except Exception as err:
                        _LOGGER.warning(f"Failed to get garage doors for location {location_id}: {err}")
                        location_data["garage_doors"] = {}

                    # Get smart locks using enhanced library
                    try:
                        smart_locks = location.get_smart_locks()
                        data["smart_locks"][location_id] = smart_locks
                        location_data["smart_locks"] = smart_locks
                        _LOGGER.info(f"Found {len(smart_locks)} smart locks for location {location_id}")
                    except Exception as err:
                        _LOGGER.warning(f"Failed to get smart locks for location {location_id}: {err}")
                        location_data["smart_locks"] = {}

                    data["locations"][location_id] = location_data

                return data

            # Execute blocking calls in executor
            return await self.hass.async_add_executor_job(get_client_data)

        except Exception as err:
            raise UpdateFailed(f"Error communicating with Total Connect: {err}")

    async def async_control_smart_lock(self, location_id: str, device_id: str, action: str) -> bool:
        """Control a smart lock using enhanced library."""
        try:
            if not self.client:
                await self._async_update_data()

            location = self.client.locations[location_id]
            result = location.control_smart_lock(device_id, action)
            _LOGGER.info(f"Smart lock {device_id} {action} result: {result}")
            return result
        except Exception as err:
            _LOGGER.error(f"Failed to control smart lock {device_id}: {err}")
            return False

    async def async_control_garage_door(self, location_id: str, device_id: str, action: str) -> bool:
        """Control a garage door using enhanced library."""
        try:
            if not self.client:
                await self._async_update_data()

            location = self.client.locations[location_id]
            result = location.control_garage_door(device_id, action)
            _LOGGER.info(f"Garage door {device_id} {action} result: {result}")
            return result
        except Exception as err:
            _LOGGER.error(f"Failed to control garage door {device_id}: {err}")
            return False
