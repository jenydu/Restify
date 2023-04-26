from django.urls import path
from .views import AllNotificationsView, NotificationDeleteView

app_name="notifications"
urlpatterns = [ 
    path('all/', AllNotificationsView.as_view(), name='all'),
    path('clear/', NotificationDeleteView.as_view(), name='clear'),
    
]