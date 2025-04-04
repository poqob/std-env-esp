"""
ESP32 Configuration Reader and Setup Module

This module reads configuration from a JSON file and sets up the 
ESP32 environment accordingly. It handles network connections,
services startup and system settings based on the configuration.

Author: Based on project by poqob
Version: 1.0.0
"""

import json
import os
import machine
import gc
from home.connection.connection import Connection
from home.connection.access_point import AP
from home.settings import frequancy, info
from home.utils.uftpd import start_ftp_server
from home.utils.command_server import CommandServer
from home.connection.ble.b import start_b
import webrepl

class Setup:
    def __init__(self, callback=None,loop=None,config_path="/config.json"):
        """Initialize the setup with config file path."""
        self.config_path = config_path
        self.config = None
        self.services = {}
        self.callback = callback
        self.loop = loop

    def run_callback(self):
        """Run the callback function if provided."""
        if self.callback:
            try:
                self.callback()
            except Exception as e:
                print(f"Callback error: {e}")
        else:
            print("No callback function provided")

        
    def read_config(self):
        """Read configuration from the JSON file."""
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.loads(file.read())
            print("Configuration loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
            
    def setup_network(self):
        """Set up network connections based on configuration."""
        if not self.config:
            return False
            
        # Setup WiFi connection
        if self.config.get("network", {}).get("wifi", {}):
            wifi_config = self.config["network"]["wifi"]
            ssid = wifi_config.get("ssid")
            password = wifi_config.get("password")
            
            # Check if static IP is enabled
            if wifi_config.get("static_ip", {}).get("enabled", False):
                static = wifi_config["static_ip"]
                self.wifi = Connection(
                    ssid, 
                    password,
                    ip=static.get("ip", ""),
                    subnet=static.get("subnet", ""),
                    gateway=static.get("gateway", ""),
                    dns=static.get("dns", "")
                )
            else:
                self.wifi = Connection(ssid, password)
                
            self.wifi.connect()
        
        # Setup Access Point if enabled
        ap_config = self.config.get("network", {}).get("access_point", {})
        if ap_config.get("enabled", False):
            self.ap = AP(
                ssid=ap_config.get("ssid", "ESP_AP"),
                password=ap_config.get("password", "password")
            )
            
        return True
            
    def setup_services(self):
        """Set up services based on configuration."""
        if not self.config:
            return False
            
        services_config = self.config.get("services", {})
        
        # Start WebREPL if enabled
        if services_config.get("webrepl", {}).get("enabled", False):
            webrepl.start()
            print("WebREPL started")
        
        # Start FTP server if enabled  
        if services_config.get("ftp", {}).get("enabled", False):
            try:
                start_ftp_server(splash=True)
                print("FTP server started")
            except Exception as e:
                print(f"Failed to start FTP server: {e}")
        
        # Start Command server if enabled
        if services_config.get("command_server", {}).get("enabled", False):
            try:
                cmd_config = services_config["command_server"]
                self.services["command_server"] = CommandServer(
                    port=cmd_config.get("port", 8080),
                    api_key=cmd_config.get("api_key", "your_secret_api_key")
                )
                self.services["command_server"].start()
            except Exception as e:
                print(f"Failed to start command server: {e}")
        
        # Start FTP server if enabled  
        if services_config.get("ble", {}).get("enabled", False):
            try:
                start_b()
                print("BLE service started")
            except Exception as e:
                print(f"Failed to start BLE service: {e}")
            
        
            
        return True
            
    def setup_system(self):
        """Configure system settings based on configuration."""
        if not self.config:
            return False
            
        system_config = self.config.get("system", {})
        
        # Set CPU frequency
        freq_setting = system_config.get("frequency", "medium").lower()
        if freq_setting == "high":
            frequancy.high_freq()
            print("CPU frequency set to high")
        elif freq_setting == "low":
            frequancy.low_freq()
            print("CPU frequency set to low")
        else:
            frequancy.mid_freq()
            print("CPU frequency set to medium")
            
        # Configure auto-restart if enabled
        if system_config.get("auto_restart", {}).get("enabled", False):
            # Implementation of auto-restart would go here
            # This would typically involve setting up a timer
            pass
            
        # Print system info if log level is appropriate
        if system_config.get("log_level", "").lower() in ["info", "debug"]:
            info.info()
            
        return True
        
    def setup_all(self):
        """Set up everything based on the configuration."""
        if not self.read_config():
            print("Using default configuration")
            return False
            
        # Set up in sequence
        print("\n--- Setting up network ---")
        self.setup_network()
        
        print("\n--- Setting up services ---")
        self.setup_services()
        
        print("\n--- Configuring system ---")
        self.setup_system()
        
        # Memory cleanup
        gc.collect()
        
        print("\n--- Setup complete ---")
        
        # Print project info
        project = self.config.get("project_info", {})
        if project:
            print(f"\nProject: {project.get('name', 'ESP32 Project')}")
            print(f"Version: {project.get('version', '1.0.0')}")
            print(f"Author: {project.get('author', '')}")
            print(f"Description: {project.get('description', '')}")
        
        return True
    
    def run_main_loop(self):
        """Run the main application loop."""
        try:
            print("\n--- Running main loop ---")
            while True:
                # Do any periodic tasks here
                machine.idle()  # Save power during idle
                if self.loop:
                    self.loop()
        except KeyboardInterrupt:
            self.cleanup()
            print("Program terminated by user")
    
    def cleanup(self):
        """Clean up and stop services before shutdown."""
        # Stop command server if running
        if "command_server" in self.services and self.services["command_server"]:
            try:
                self.services["command_server"].stop()
                print("Command server stopped")
            except:
                pass
        
        

def create_default_config():
    """Create a default configuration file if none exists."""
    if "config.json" not in os.listdir("/"):
        default_config = {
            "network": {
                "wifi": {
                    "ssid": "your_ssid",
                    "password": "your_password",
                    "static_ip": {
                        "enabled": False
                    }
                },
                "access_point": {
                    "enabled": True,
                    "ssid": "ESP32_AP",
                    "password": "password123"
                }
            },
            "services": {
                "webrepl": {"enabled": True},
                "ftp": {"enabled": True},
                "command_server": {
                    "enabled": True,
                    "port": 8080,
                    "api_key": "change_this_key"
                },
                "ble": {"enabled": False}
            },
            "system": {
                "frequency": "medium",
                "auto_restart": {"enabled": False},
                "log_level": "info"
            }
        }
        
        try:
            with open("/config.json", "w") as f:
                f.write(json.dumps(default_config))
            print("Created default configuration file")
        except:
            print("Failed to create default configuration file")

# For standalone testing
if __name__ == "__main__":
    if "config.json" not in os.listdir("/"):
        create_default_config()
    setup = Setup()
    setup.setup_all()