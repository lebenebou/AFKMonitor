
import urllib.request
import psutil

class InternetState:

    def __init__(self, isConnected: bool, bytesSent: float, bytesRecv: float):
        
        self.isConnected = isConnected
        self.bytesSent = bytesSent
        self.bytesRecv = bytesRecv

def isConnected() -> bool:

    websitesToCheck = ["https://www.google.com", "https://www.microsoft.com", "https://www.apple.com"]

    for website in websitesToCheck:

        try:
            urllib.request.urlopen(website, timeout=5)
            return True
        except:
            continue

    return False

def getInternetState() -> InternetState:

    ioCounters = psutil.net_io_counters()
    return InternetState(isConnected(), ioCounters.bytes_sent, ioCounters.bytes_recv)