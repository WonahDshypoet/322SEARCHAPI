from django.shortcuts import render
from django.views import View
from .forms import SearchForm
from .document_parser import DocumentParser
from .indexer import Indexer
from .query import Query
from .ranking import Ranking
from .results_page import ResultsPage
from .models import Document, InvertedIndex


class SearchView(View):
    template_name = 'search.html'

    def get(self, request):
        form = SearchForm()
        return render(request, self.template_name, {'form': form, 'results': []})

    def post(self, request):
        form = SearchForm(request.POST)
        results = []

        if form.is_valid():
            query_string = form.cleaned_data['query']

            # Create a document parser and indexer
            document_parser = DocumentParser(Document)
            indexer = Indexer(document_parser, InvertedIndex)

            # Create a query and set the query string
            query = Query(indexer)
            query.set_query(query_string)

            # Execute the query and get the search results
            search_results = query.execute()

            # Run ranking algorithm
            ranking = Ranking(indexer)
            ranked_results = ranking.rank_results(query, search_results)

            # Create an instance of ResultsPage and display the results
            results_page = ResultsPage()
            results_page.display_results(ranked_results)

            # Retrieve the results for passing to the template
            results = results_page.results

        return render(request, self.template_name, {'form': form, 'results': results})
