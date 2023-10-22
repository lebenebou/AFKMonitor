
import urllib.request

def isConnected() -> bool:
    try:
        urllib.request.urlopen("https://www.google.com", timeout=1)
        return True
    except Exception:
        return False