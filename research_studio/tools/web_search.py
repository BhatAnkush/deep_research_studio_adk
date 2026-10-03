from ddgs import DDGS

MAX_RESULTS = 5


def web_search(query: str) -> dict:
    """Searches the web and returns the top results.

    Use this for recent, changing, or uncertain facts.

    Args:
        query: The search query, in plain words.

    Returns:
        A dict with status "success" and a list of results (title, link,
        snippet), or status "error" with an error_message.
    """
    try:
        with DDGS() as client:
            raw = client.text(query, max_results=MAX_RESULTS)

        results = [
            {
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in raw
        ]
        return {"status": "success", "query": query, "results": results}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}