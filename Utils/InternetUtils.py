
import urllib.request

def isConnected() -> bool:

    websites_to_check = ["https://www.google.com", "https://www.microsoft.com", "https://www.apple.com"]

    for website in websites_to_check:

        try:
            urllib.request.urlopen(website, timeout=5)
            return True
        except (urllib.error.URLError, ConnectionError):
            continue

    return False