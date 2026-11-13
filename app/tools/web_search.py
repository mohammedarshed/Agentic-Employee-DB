def web_search(query: str, max_results: int = 5):
    """Search the web (DuckDuckGo, no API key needed) and return top results."""

    # Imported lazily so the rest of the agent still works if the
    # package is missing; the error is reported back to the LLM instead.
    from ddgs import DDGS

    max_results = max(1, min(int(max_results), 10))

    results = DDGS().text(query, max_results=max_results)

    return [
        {
            "title": r.get("title"),
            "url": r.get("href"),
            "snippet": r.get("body")
        }
        for r in results
    ]
