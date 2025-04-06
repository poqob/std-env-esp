# main.py
from micropython import const
import time
from machine import Pin

MANIFEST = const('I am Dağ, a Turkish guy who loves her country 🇹🇷.')

def once():
    print(MANIFEST)
    

led = Pin(2, Pin.OUT)

def main():
    led.value(1)
    time.sleep(0.25)
    led.value(0)
    time.sleep(0.25)
    
    