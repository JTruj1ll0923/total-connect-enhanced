# Total Connect Enhanced

**Total Connect Enhanced** is a Home Assistant custom integration that provides full support for Total Connect 2.0 systems, including garage door openers and smart locks.

## Features

- ✅ **Smart Lock Control** - Lock and unlock smart locks via Total Connect
- ✅ **Garage Door Control** - Open and close garage doors via MyQ integration
- ✅ **Real-time Status** - Monitor device status and state changes
- ✅ **Automatic Discovery** - Automatically finds and configures devices
- ✅ **Error Handling** - Robust error handling and retry logic
- ✅ **HACS Integration** - Easy installation and updates via HACS

## Supported Devices

- **Smart Locks** - Z-Wave and WiFi smart locks paired with Total Connect
- **Garage Doors** - MyQ garage door openers integrated with Total Connect
- **Security Systems** - Basic security system monitoring

## Installation

### Via HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Add this repository to HACS:
   - Go to HACS > Integrations
   - Click the three dots menu > Custom Repositories
   - Add: `https://github.com/justincase/total-connect-enhanced`
   - Category: Integration
3. Install "Total Connect Enhanced" from HACS
4. Restart Home Assistant
5. Add the integration in Settings > Devices & Services

### Manual Installation

1. Download the latest release
2. Copy the `totalconnect_enhanced` directory to `/config/custom_components/`
3. Restart Home Assistant
4. Add the integration in Settings > Devices & Services

## Configuration

1. Go to **Settings > Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Total Connect Enhanced"**
4. Enter your Total Connect credentials:
   - **Username**: Your Total Connect username
   - **Password**: Your Total Connect password
   - **User Code**: Your alarm user code (default: 1234)

## Usage

### Smart Locks

Once configured, smart locks will appear as **Lock entities**:

```yaml
# Example automation
automation:
  - alias: Lock Front Door at Night
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: lock.lock
        target:
          entity_id: lock.front_door
```

### Garage Doors

Garage doors will appear as **Cover entities**:

```yaml
# Example automation
automation:
  - alias: Close Garage Door at Night
    trigger:
      - platform: time
        at: "23:00:00"
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.garage_door
```

### Services

Additional services are available for advanced control:

```yaml
# Control smart lock
service: totalconnect_enhanced.control_smart_lock
data:
  entity_id: lock.front_door
  action: unlock

# Control garage door
service: totalconnect_enhanced.control_garage_door
data:
  entity_id: cover.garage_door
  action: open
```

## Troubleshooting

### Devices Not Appearing

1. **Check Total Connect App**: Ensure devices are paired and visible in the Total Connect mobile app
2. **Verify Credentials**: Double-check your username, password, and user code
3. **Check Logs**: Look for error messages in Home Assistant logs
4. **Restart Integration**: Try restarting the integration in Settings > Devices & Services

### Control Not Working

1. **Device Online**: Ensure devices are online and connected
2. **Permissions**: Verify your account has device control permissions
3. **Network**: Check your internet connection
4. **Retry**: The integration includes automatic retry logic

### Debug Mode

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.totalconnect_enhanced: debug
```

## Development

This integration is based on the enhanced `total-connect-client` library with:

- **SOAP API Support** for device control
- **REST API Integration** for status monitoring
- **Real Device Testing** with actual Total Connect systems
- **Home Assistant Best Practices** for integration development

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/justincase/total-connect-enhanced/issues)
- **Discussions**: [GitHub Discussions](https://github.com/justincase/total-connect-enhanced/discussions)

## Acknowledgments

- Based on the original [total-connect-client](https://github.com/craigjmidwinter/total-connect-client) library
- Enhanced with garage door and smart lock support
- Built with Home Assistant integration best practices
