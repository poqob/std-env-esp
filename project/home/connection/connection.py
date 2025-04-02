"""
MicroPython WiFi Connection Manager for ESP devices

Author: Dağ
Creation Date: April 3, 2025
Version: 1.0.0

This module provides a simple interface for connecting an ESP device
to a WiFi network with options for static IP configuration.
"""

import network
import time
class Connection:
    def __init__(self, ssid, password,ip='',subnet='',gateway='' , dns='' ):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        
        #configuration
        if ip!='':
            # Set the static IP configuration
            self.sta_if.ifconfig((ip, subnet, gateway, dns))
        # mac adress
        self.mac = self.sta_if.config('mac')
        # ip address
        print("IP: ",self.sta_if.ifconfig()[0])
        print("MAC:",self.mac.hex())

    def connect(self, timeout=15):
        self.sta_if.connect(self.ssid, self.password)
        
        print("Connecting to network...")

        start_time = time.time()
        while not self.sta_if.isconnected():
            if time.time() - start_time > timeout:
                print("Connection timeout.")
                return False
            print(".")
            time.sleep(1)

        if self.sta_if.isconnected():
            print("Network config:", self.sta_if.ifconfig())
            return True
        else:
            return False
