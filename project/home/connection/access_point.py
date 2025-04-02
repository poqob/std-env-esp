"""
MicroPython Access Point Manager for ESP devices

Author: Dağ
Creation Date: April 3, 2025
Version: 1.0.0
License: MIT License

This module provides a simple interface for creating and managing 
an access point on ESP devices with various configuration options.
"""

import network

class AP:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.ap = network.WLAN(network.AP_IF)
        self.start()
        self.ap.config(essid=self.ssid, authmode=3,password=self.password) # authmode 3 is WPA2-PSK
            
        
    def start(self):
        if not self.ap.active():
            self.ap.active(True)
            print("Access Point started")
        else:
            print("Access Point already active")
    def stop(self):
        if self.ap.active():
            self.ap.active(False)
            print("Access Point stopped")
    def status(self):
        if self.ap.active():
            print("Access Point is active")
        else:
            print("Access Point is inactive")
    def get_ip(self):
        if self.ap.active():
            ip = self.ap.ifconfig()[0]
            print("Access Point IP address:", ip)
        else:
            print("Access Point is inactive, cannot get IP address")
    def get_clients(self):
        if self.ap.active():
            clients = self.ap.status('stations')
            print("Connected clients:", clients)
        else:
            print("Access Point is inactive, cannot get connected clients")
    def get_config(self):
        if self.ap.active():
            config = self.ap.ifconfig()
            print("Access Point configuration:", config)
        else:
            print("Access Point is inactive, cannot get configuration")
    def get_essid(self):
        if self.ap.active():
            essid = self.ap.config('essid')
            print("Access Point ESSID:", essid)
        else:
            print("Access Point is inactive, cannot get ESSID")
    def get_password(self):
        if self.ap.active():
            password = self.ap.config('password')
            print("Access Point Password:", password)
        else:
            print("Access Point is inactive, cannot get password")
    def get_mac(self):
        if self.ap.active():
            mac = self.ap.config('mac')
            print("Access Point MAC address:", mac)
        else:
            print("Access Point is inactive, cannot get MAC address")
    def get_channel(self):
        if self.ap.active():
            channel = self.ap.config('channel')
            print("Access Point Channel:", channel)
        else:
            print("Access Point is inactive, cannot get channel")
    
    def get_authmode(self):
        if self.ap.active():
            authmode = self.ap.config('authmode')
            print("Access Point Auth Mode:", authmode)
        else:
            print("Access Point is inactive, cannot get auth mode")
