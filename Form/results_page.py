
class ResultsPage:
    def __init__(self):
        self.results = []

    def display_results(self, search_results):
        # Implement the logic to display the search results on the page
        self.results = search_results
        for result in self.results:
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            snippet = self.get_snippet(result['content'], result['query'])
            print(f"Snippet: {snippet}")
            print("\n")

    def get_snippet(self, content, query):
        # Implement the logic to generate a snippet from the content for display
        query_terms = query.split()
        content_words = content.split()
        snippet_length = 20  # Number of words in the snippet

        for i in range(len(content_words)):
            if all(term in content_words[i:i+len(query_terms)] for term in query_terms):
                snippet_start = max(0, i - snippet_length // 2)
                snippet_end = min(len(content_words), i + len(query_terms) + snippet_length // 2)
                snippet_words = content_words[snippet_start:snippet_end]
                snippet = ' '.join(snippet_words)
                return snippet

        # If no exact match is found, return the first few words from the content
        snippet = ' '.join(content_words[:snippet_length])
        return snippet
