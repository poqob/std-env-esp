"""
MicroPython System Information Utility for ESP devices

Author: Dağ
Creation Date: April 3, 2025
Version: 1.0.0
License: MIT License

This module provides functions to retrieve and display system information
about ESP devices including chip model, CPU frequency, memory usage and hardware features.
"""

import machine
import esp32

def modules():
    help('modules')


def info():
    # Get ESP32 chip model
    print("Chip Model:", machine.__name__)  # Usually 'esp32' or 'esp32s2/s3/c3'

    # CPU frequency (MHz)
    print("CPU Freq:", machine.freq() / 1_000_000, "MHz")

    # Check if it's dual-core (ESP32)
    try:
        print("Cores:", esp32.HEAP_DATA if hasattr(esp32, 'HEAP_DATA') else "Single-core?")
    except:
        print("Core info not available.")
        
        
    import gc
    import micropython

    # Total & Free Heap RAM
    print("Free RAM:", round(gc.mem_free()/(1024),2), "Kbyte")
    print("Total RAM:", round((gc.mem_alloc() + gc.mem_free())/(1024),2), "Kbyte")

    # Check if PSRAM (SPIRAM) is available (ESP32-WROVER)
    try:
        if esp32.PSRAM:
            print("PSRAM available:", round(esp32.PSRAM.size()/(1024),2), "Kbyte")
    except:
        print("No PSRAM detected.")

