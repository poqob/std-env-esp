#conf.py
import machine

def high_freq():
    machine.freq(240_000_000)

def mid_freq():
    machine.freq(160_000_000)
    
def low_freq():
    machine.freq(80_000_000)
