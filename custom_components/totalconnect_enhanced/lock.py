"""Lock platform for Total Connect Enhanced smart locks."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEVICE_TYPE_SMART_LOCK

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Total Connect Enhanced lock platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    locks = []
    
    for location_id, location_data in coordinator.data["locations"].items():
        for device_id, device in location_data.get("smart_locks", {}).items():
            locks.append(
                TotalConnectSmartLock(
                    coordinator,
                    entry,
                    location_id,
                    device_id,
                    device,
                )
            )

    async_add_entities(locks, True)


class TotalConnectSmartLock(LockEntity):
    """Representation of a Total Connect smart lock."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        location_id: str,
        device_id: str,
        device: Any,
    ) -> None:
        """Initialize the smart lock."""
        self.coordinator = coordinator
        self._entry = entry
        self._location_id = location_id
        self._device_id = device_id
        self._device = device
        self._is_locked = False

        self._attr_name = device.name
        self._attr_unique_id = f"lock_{device_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device.name,
            manufacturer="Total Connect",
            model="Smart Lock",
        )

    @property
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return self._is_locked

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the lock."""
        success = await self.coordinator.async_control_smart_lock(
            self._location_id, self._device_id, "lock"
        )
        if success:
            self._is_locked = True
            self.async_write_ha_state()
        else:
            _LOGGER.error(f"Failed to lock {self._device.name}")

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the lock."""
        success = await self.coordinator.async_control_smart_lock(
            self._location_id, self._device_id, "unlock"
        )
        if success:
            self._is_locked = False
            self.async_write_ha_state()
        else:
            _LOGGER.error(f"Failed to unlock {self._device.name}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Update lock state based on coordinator data
        # For now, we'll keep the current state
        # In a real implementation, you'd parse the device status
        self.async_write_ha_state()
