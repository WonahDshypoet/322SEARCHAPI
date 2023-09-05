from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    # path('results/<int:result_id>/', views.ResultDetailView.as_view(), name='result_detail'),
]
