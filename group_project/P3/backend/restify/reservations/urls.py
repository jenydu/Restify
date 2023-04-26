from django.urls import path
from .views import AllReservationsView, Create, RequestCancel, Terminate, ApproveDenyPending, ApproveDenyCancel

app_name="reservations"
urlpatterns = [ 
    path('all/', AllReservationsView.as_view(), name='all'),
    path('create/', Create.as_view(), name='create'),
    path('cancel/', RequestCancel.as_view(), name='cancel'),
    path('terminate/', Terminate.as_view(), name='terminate'),
    path('approve/pending/', ApproveDenyPending.as_view(), name='ApproveDenyPending'),
    path('approve/cancel/', ApproveDenyCancel.as_view(), name='ApproveDenyCancel'),
]