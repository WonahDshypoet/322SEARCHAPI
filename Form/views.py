
from django.shortcuts import render
from .models import Document
from .indexer import Indexer
from .query import Query
from .ranking import Ranking
from .results_page import ResultsPage


def search_view(request):
    results = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data['query']

            # Assuming you have already initialized the Indexer object
            indexer = Indexer(document_parser, db_repository)
            query = Query(indexer)
            query.set_query(query_string)

            # Execute the query and get the search results
            search_results = query.execute()

            # Assuming you have already initialized the Ranking object
            ranking = Ranking(indexer)
            ranked_results = ranking.rank_results(query, search_results)

            # Display the results using the ResultsPage class
            results_page = ResultsPage()
            results_page.display_results(ranked_results)

            # Populate the 'results' list with the ranked search results
            results = ranked_results
    else:
        form = SearchForm()

    return render(request, 'search_results.html', {'form': form, 'results': results})
