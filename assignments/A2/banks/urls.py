from django.urls import path
from .views import BankCreateView, BranchCreateView, BranchDetailsView, AllBranchesView, BankListView, BankDetailView, BranchUpdateView

app_name = 'banks'
urlpatterns = [
    path("add/", BankCreateView.as_view(), name="bank_add"),
    path('<bank_id>/branches/add/', BranchCreateView.as_view(), name="branch_add"),

    path('branch/<branch_id>/details/', BranchDetailsView.as_view(), name='branch_details'),
    path('<bank_id>/branches/all/', AllBranchesView.as_view(), name='all_branches'),

    path('all/', BankListView.as_view(), name='bank_list'),
    path('<bank_id>/details/', BankDetailView.as_view(), name='bank_detail'),
    path('branch/<pk>/edit/', BranchUpdateView.as_view(), name='branch_edit'),
]