from ddgs import DDGS

def search_web(query):
    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=3)

            for r in search_results:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "content": r.get("body", "")
                })

        # Handle empty search results
        if not results:
            results.append({
                "title": "No results found",
                "url": "",
                "content": f"No search results found for query: {query}"
            })

    except Exception as e:
        results.append({
            "title": "Search Error",
            "url": "",
            "content": f"Web search error: {str(e)}"
        })

    return results