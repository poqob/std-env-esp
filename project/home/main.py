# main.py
from home.connection.connection import Connection
from home.connection.uftpd import start_ftp_server
from home.settings import info, frequancy
from home.connection.access_point import AP

from home.connection.ble.b import start_b
import webrepl

def main32():
    conn = Connection("merkur", "merkur.online")#, ip, subnet, gateway, dns)
    conn.connect() # connect to the network
    webrepl.start() # connect your device with webrepl ip:port
    ap=AP(ssid="saturn", password="saturn123") # turn on AP to connect ftp server locally
    start_ftp_server() # start ftp server to upload and download files
    frequancy.mid_freq() # set the frequancy to 160MHz
    info.info() # get the info about the device and current status
    # start_b() # start the ble uart terminal
    