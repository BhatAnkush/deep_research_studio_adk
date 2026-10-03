import requests
import bs4

MAX_CHARS = 6000


def parse_html(html: str) -> bs4.BeautifulSoup:
    """Parses an HTML string into a BeautifulSoup object."""
    return bs4.BeautifulSoup(html, "html.parser")


def fetch_url(url: str) -> dict:
    """Fetches a web page and returns its readable text.

    Use this when you need the contents of a specific URL.

    Args:
        url: The full web address, starting with http:// or https://.

    Returns:
        A dict with status "success", the url and the page text,
        or status "error" with an error_message.
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        return {"status": "error", "error_message": "Invalid URL"}

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = parse_html(response.text)
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return {"status": "success", "url": url, "text": text[:MAX_CHARS]}
    except requests.RequestException as e:
        return {"status": "error", "error_message": str(e)}