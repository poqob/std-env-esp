# ESP Standard Development Environment

This repository contains a standard development environment template for ESP boards using MicroPython. The project provides a ready-to-use framework with WiFi connection management, access point configuration, FTP server functionality, BLE connectivity, and system utilities.

## Project Structure

```
std-env-esp/
│
├── app                  # Executable FTP tool for file transfer
├── _.remove             # Related to FTP tool
│
└── project/
    ├── boot.py          # Entry point that loads setup and calls main
    ├── config.json      # Configuration file for all services
    ├── webrepl_cfg.py   # WebREPL configuration
    │
    ├── home/
    │   ├── main.py      # Main application code
    │   ├── setup.py     # Configuration loader and setup module
    │   │
    │   ├── connection/  # Network connectivity modules
    │   │   ├── access_point.py   # AP management
    │   │   ├── connection.py     # WiFi client connection
    │   │   │
    │   │   └── ble/     # Bluetooth Low Energy modules
    │   │       ├── b.py                 # BLE service implementation
    │   │       ├── ble_advertising.py   # BLE advertising helpers
    │   │       └── ble_uart_peripheral.py # BLE UART implementation
    │   │
    │   ├── utils/       # Utility modules
    │   │   ├── uftpd.py          # FTP server implementation
    │   │   └── command_server.py # HTTP API command server
    │   │
    │   └── settings/    # System configuration modules
    │       ├── frequancy.py     # CPU frequency management
    │       └── info.py          # System information utilities
    │
    └── lib/             # External libraries (binary format)
        ├── base64.mpy
        ├── binascii.mpy
        ├── pickle.mpy
        └── zlib.mpy
```

## Features

- **WiFi Connection Management**: Easy connection to WiFi networks with static IP support
- **Access Point Configuration**: Create and manage WiFi access points
- **WebREPL Support**: Remote Python REPL via WebSocket connection
- **FTP Server**: Built-in FTP server for convenient file transfers
- **BLE Connectivity**: Bluetooth Low Energy UART service
- **Command Server**: HTTP API for remote command execution and device control
- **System Information**: Utilities to monitor ESP system information
- **CPU Frequency Control**: Adjust CPU frequency for power/performance balance
- **JSON Configuration**: All settings managed through a central config file

## Getting Started

1. Flash MicroPython firmware to your ESP board
2. Upload the entire `project` directory to your ESP
3. Edit `config.json` to configure your device (WiFi settings, services, etc.)
4. The system will automatically:
   - Connect to the configured WiFi network
   - Start WebREPL service (if enabled)
   - Create an access point (if enabled)
   - Start the FTP server (if enabled)
   - Start the command server (if enabled)
   - Start BLE services (if enabled)
   - Set CPU frequency according to configuration
   - Display system information

## Configuration

The `config.json` file controls all aspects of the environment:

```json
{
  "network": {
    "wifi": {
      "ssid": "your_wifi_name",
      "password": "your_wifi_password",
      "static_ip": {
        "enabled": false,
        "ip": "192.168.1.100",
        "subnet": "255.255.255.0",
        "gateway": "192.168.1.1",
        "dns": "8.8.8.8"
      }
    },
    "access_point": {
      "enabled": true,
      "ssid": "ESP_AP_NAME",
      "password": "ap_password"
    }
  },
  "services": {
    "webrepl": {
      "enabled": true,
      "password": "webrepl_password"
    },
    "ftp": {
      "enabled": true
    },
    "command_server": {
      "enabled": true,
      "port": 8080,
      "api_key": "your_secret_key"
    },
    "ble": {
      "enabled": false
    }
  },
  "system": {
    "frequency": "medium",  // low, medium, high
    "auto_restart": {
      "enabled": false,
      "interval_hours": 24
    },
    "log_level": "info"
  }
}
```

## Usage Examples

### Connect to a WiFi Network

```python
from home.connection.connection import Connection

# Connect to WiFi with DHCP
wifi = Connection("your_ssid", "your_password")
wifi.connect()

# Connect with static IP
wifi = Connection("your_ssid", "your_password", 
                  ip="192.168.1.100", 
                  subnet="255.255.255.0", 
                  gateway="192.168.1.1", 
                  dns="8.8.8.8")
wifi.connect()
```

### Create an Access Point

```python
from home.connection.access_point import AP

# Create and start an access point
ap = AP("ESP_AP", "password123")

# Get AP information
ap.get_ip()
ap.get_config()
ap.get_clients()
ap.get_mac()
ap.get_channel()
```

### Use the Command Server

```python
# The command server provides an HTTP API for remote control
# Example API call to restart the device:
# POST /restart with JSON body: {"api_key": "your_secret_api_key"}

from home.utils.command_server import CommandServer
server = CommandServer(port=8080, api_key="secure_key")
server.start()
```

### Enable BLE UART Service

```python
# Start BLE UART service for wireless communication
from home.connection.ble.b import start_b
start_b()  # Starts BLE service with name "SaturnBLE"
```

### Manage CPU Frequency

```python
from home.settings import frequancy

# Set different CPU frequencies
frequancy.high_freq()  # 240MHz
frequancy.mid_freq()   # 160MHz
frequancy.low_freq()   # 80MHz
```

### Get System Information

```python
from home.settings import info

# Display system information
info.info()

# List available modules
info.modules()
```

## File Transfer Tool

The included `app` executable is an FTP client tool for transferring files to/from your ESP. Source code for this tool is available at: https://github.com/poqob/ftp-tool.git

### Setting Up File Transfer

1. The ESP must be running the `uftpd.py` server (included in this project)
2. Make sure the ESP is connected to your network or you're connected to its access point
3. Ensure the executable has execute permissions (`chmod +x app` if needed)
4. Run `./app` to start the FTP client tool

If you need to modify or build the tool from source, clone the repository and follow the build instructions provided there.

## Using WebREPL

When WebREPL is enabled:

1. Connect to the ESP's WiFi network or ensure it's on your network
2. Visit http://micropython.org/webrepl/
3. Connect to the device's IP address
4. Enter the WebREPL password (default: "esp32")
5. You now have a remote Python terminal to execute commands

## License

MIT License