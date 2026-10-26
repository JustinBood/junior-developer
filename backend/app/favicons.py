from urllib.parse import urlparse

FAVICON_SERVICE = "https://www.google.com/s2/favicons?domain={domain}&sz=64"


def favicon_url(url: str) -> str:
    """The favicon for the website that url is on."""
    domain = urlparse(url).netloc
    return FAVICON_SERVICE.format(domain=domain)