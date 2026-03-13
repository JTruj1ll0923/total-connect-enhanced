"""Sensor platform for Total Connect Enhanced devices."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Total Connect Enhanced sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    
    for location_id, location_data in coordinator.data["locations"].items():
        # Add location status sensors
        sensors.append(
            TotalConnectLocationSensor(
                coordinator,
                entry,
                location_id,
                location_data,
            )
        )
        
        # Add garage door status sensors
        for garage_id, garage_info in location_data.get("garage_doors", {}).items():
            sensors.append(
                TotalConnectGarageDoorSensor(
                    coordinator,
                    entry,
                    location_id,
                    garage_id,
                    garage_info,
                )
            )

    async_add_entities(sensors, True)


class TotalConnectLocationSensor(SensorEntity):
    """Representation of a Total Connect location status sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        location_id: str,
        location_data: Dict[str, Any],
    ) -> None:
        """Initialize the location sensor."""
        self.coordinator = coordinator
        self._entry = entry
        self._location_id = location_id

        self._attr_name = f"{location_data['name']} Status"
        self._attr_unique_id = f"sensor_{location_id}_status"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        location_data = self.coordinator.data["locations"].get(self._location_id, {})
        return "Connected" if location_data else "Disconnected"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._location_id in self.coordinator.data.get("locations", {})

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


class TotalConnectGarageDoorSensor(SensorEntity):
    """Representation of a Total Connect garage door status sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        location_id: str,
        garage_id: str,
        garage_info: Dict[str, Any],
    ) -> None:
        """Initialize the garage door sensor."""
        self.coordinator = coordinator
        self._entry = entry
        self._location_id = location_id
        self._garage_id = garage_id
        self._garage_info = garage_info

        self._attr_name = f"{garage_info['name']} State"
        self._attr_unique_id = f"sensor_{garage_id}_state"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, garage_id)},
            name=garage_info["name"],
            manufacturer="Total Connect",
            model="Garage Door",
        )

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        location_data = self.coordinator.data["locations"].get(self._location_id, {})
        garage_doors = location_data.get("garage_doors", {})
        
        if self._garage_id in garage_doors:
            return garage_doors[self._garage_id].get("state", "unknown")
        
        return "unknown"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        location_data = self.coordinator.data["locations"].get(self._location_id, {})
        garage_doors = location_data.get("garage_doors", {})
        return self._garage_id in garage_doors

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        location_data = self.coordinator.data["locations"].get(self._location_id, {})
        garage_doors = location_data.get("garage_doors", {})
        
        if self._garage_id in garage_doors:
            garage_info = garage_doors[self._garage_id]
            return {
                "online": garage_info.get("online"),
                "switch_id": garage_info.get("switch_id"),
                "can_remote_close": garage_info.get("can_remote_close"),
                "battery_low": garage_info.get("battery_low"),
            }
        
        return {}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
