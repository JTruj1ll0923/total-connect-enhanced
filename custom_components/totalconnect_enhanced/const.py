"""Constants for Total Connect Enhanced integration."""

from homeassistant.const import Platform

DOMAIN = "totalconnect_enhanced"

# Device types
DEVICE_TYPE_SMART_LOCK = "smart_lock"
DEVICE_TYPE_GARAGE_DOOR = "garage_door"

# Platforms
PLATFORMS = [
    Platform.LOCK,
    Platform.COVER,
    Platform.SENSOR,
]

# Configuration keys
CONF_USERCODE = "usercode"

# Update intervals
SCAN_INTERVAL = timedelta(seconds=30)
