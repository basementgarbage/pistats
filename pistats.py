import os
import psutil
from os import system, name
import socket
import pystyle
from pystyle import Colors, Colorate
import time
import platform
from datetime import datetime
import urllib.request

#this is the delay between the stats updating.
#this is also in seconds
UPDATE_DELAY = 2 


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


io = psutil.net_io_counters()
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

while True:
    if name == 'nt':
        print(Colorate.Horizontal(Colors.blue_to_white, "PiStats on windows!", 1))
        print(Colors.blue + """
    .----------------.
   |          _       |
   |      _.-'|'-._   |
   | .__.|    |    |  |
   |     |_.-'|'-._|  | WINDOWS !
   | '--'|    |    |  |
   | '--'|_.-'`'-._|  |
   | '--'          `  |
    '----------------'
        """ )
    else:
        print("pistats - wk2poor")
        print(Colors.green + """
.~~.   .~~.
'. \ ' ' / .'
        """, Colors.red + f"""
   .~ .~~~..~.
  : .~.'~'.~. :
 ~ (   ) (   ) ~
( : '~'.~.'~' : )
 ~ .~ (   ) ~. ~
  (  : '~' :  ) Raspberry Pi : {socket.gethostname()}
   '~ .~~~. ~'
       '~'
        """)
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15/os.cpu_count()) * 100
    boottxt = "=== UPTIME ==="
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(Colors.yellow + boottxt)
    print(Colors.white + f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    specstxt = "=== SPECS ==="
    print(Colors.red + specstxt + Colors.white)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    usagetxt = "=== USAGE ==="
    print(Colors.green + usagetxt + Colors.white)
    print("CPU Usage :", psutil.cpu_percent())
    print('RAM memory % used:', psutil.virtual_memory()[2])
    print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
    networktxt = "=== NETWORK ==="
    print(Colors.blue + networktxt + Colors.white)
    print("Hostname:", socket.gethostname())
    print("local IP", socket.gethostbyname(socket.gethostname()))
    print("IPv4", external_ip)
    io_2 = psutil.net_io_counters()
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    print(f"Upload: {get_size(io_2.bytes_sent)}\n"
          f"Download: {get_size(io_2.bytes_recv)}\n"
          f"Upload Speed: {get_size(us / UPDATE_DELAY)}/s\n"
          f"Download Speed: {get_size(ds / UPDATE_DELAY)}/s", end="\r")
    # update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
    time.sleep(UPDATE_DELAY)
    clear()
