from django.urls import path
from .views import Create, Update, Search, Delete, DeleteAvailability

app_name="properties"
urlpatterns = [ 
    path('create/', Create.as_view(), name='create'),
    path('update/<int:pk>/', Update.as_view(), name='update'),
    path('search/', Search.as_view(), name='search'),
    path('delete/<int:pk>/', Delete.as_view(), name='delete'),
    path('delete/availability/<int:pk>/', DeleteAvailability.as_view(), name='delete-avail')
]