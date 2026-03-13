"""Cover platform for Total Connect Enhanced garage doors."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEVICE_TYPE_GARAGE_DOOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Total Connect Enhanced cover platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    covers = []
    
    for location_id, location_data in coordinator.data["locations"].items():
        for garage_id, garage_info in location_data.get("garage_doors", {}).items():
            covers.append(
                TotalConnectGarageDoor(
                    coordinator,
                    entry,
                    location_id,
                    garage_id,
                    garage_info,
                )
            )

    async_add_entities(covers, True)


class TotalConnectGarageDoor(CoverEntity):
    """Representation of a Total Connect garage door."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        location_id: str,
        garage_id: str,
        garage_info: Dict[str, Any],
    ) -> None:
        """Initialize the garage door."""
        self.coordinator = coordinator
        self._entry = entry
        self._location_id = location_id
        self._garage_id = garage_id
        self._garage_info = garage_info

        self._attr_name = garage_info["name"]
        self._attr_unique_id = f"cover_{garage_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, garage_id)},
            name=garage_info["name"],
            manufacturer="Total Connect",
            model="Garage Door",
        )
        self._attr_supported_features = (
            CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE
        )

    @property
    def is_closed(self) -> bool:
        """Return true if the garage door is closed."""
        return self._garage_info.get("state") == "closed"

    @property
    def is_opening(self) -> bool:
        """Return true if the garage door is opening."""
        return self._garage_info.get("state") == "opening"

    @property
    def is_closing(self) -> bool:
        """Return true if the garage door is closing."""
        return self._garage_info.get("state") == "closing"

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the garage door."""
        success = await self.coordinator.async_control_garage_door(
            self._location_id, self._garage_id, "open"
        )
        if success:
            self._garage_info["state"] = "opening"
            self.async_write_ha_state()
        else:
            _LOGGER.error(f"Failed to open {self._garage_info['name']}")

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the garage door."""
        success = await self.coordinator.async_control_garage_door(
            self._location_id, self._garage_id, "close"
        )
        if success:
            self._garage_info["state"] = "closing"
            self.async_write_ha_state()
        else:
            _LOGGER.error(f"Failed to close {self._garage_info['name']}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Update garage door state from coordinator data
        location_data = self.coordinator.data["locations"].get(self._location_id, {})
        garage_doors = location_data.get("garage_doors", {})
        
        if self._garage_id in garage_doors:
            self._garage_info = garage_doors[self._garage_id]
            self.async_write_ha_state()
