from django.urls import path
from search import views

app_name='search'
urlpatterns = [
    path('search_products',views.search_products,name='search_products'),
]

