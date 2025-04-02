# ESP Standard Development Environment

This repository contains a standard development environment template for ESP boards using MicroPython. The project provides a ready-to-use framework with WiFi connection management, access point configuration, FTP server functionality, and system utilities.

## Project Structure

```
standart_enviroment/
│
├── app                  # Executable FTP tool for file transfer
├── _.remove             # Related to FTP tool
│
└── project/
    ├── boot.py          # Entry point that calls main32 function
    ├── webrepl_cfg.py   # WebREPL configuration
    │
    ├── home/
    │   ├── main.py      # Main application code
    │   │
    │   ├── connection/  # Network connectivity modules
    │   │   ├── access_point.py   # AP management
    │   │   ├── connection.py     # WiFi client connection
    │   │   └── uftpd.py          # FTP server implementation
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
- **System Information**: Utilities to monitor ESP system information
- **CPU Frequency Control**: Adjust CPU frequency for power/performance balance

## Getting Started

1. Flash MicroPython firmware to your ESP board
2. Upload the entire `project` directory to your ESP
3. The system will automatically:
   - Connect to the WiFi network 
   - Start WebREPL service
   - Create an access point named 
   - Start an FTP server
   - Set CPU frequency to medium (160MHz)
   - Display system information

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
```

## File Transfer Tool

The included `app` executable is an FTP client tool for transferring files to/from your ESP. Source code for this tool is available at: https://github.com/poqob/ftp-tool.git

### Setting Up

1. The ESP must be running the `uftpd.py` server (included in this project)
2. Make sure the ESP is connected to your network or you're connected to its access point
3. The executable has permissions to run (`chmod +x app` if needed)

The source code for this FTP tool is available at: https://github.com/poqob/ftp-tool.git

If you need to modify or build the tool from source, clone the repository and follow the build instructions provided there.