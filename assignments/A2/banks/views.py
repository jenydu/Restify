
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError

from .forms import CreateBranchForm, CreateBankForm
from .models import Bank, Branch

class AuthenticatedView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        return super().dispatch(request, *args, **kwargs)

class BankCreateView(AuthenticatedView, CreateView):
    template_name = 'banks/create.html'
    form_class = CreateBankForm
    model = Bank

    def get_success_url(self):
        bank_id = self.object.id
        return ('/banks/%s/details/' % bank_id )
    
    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        return super().form_valid(form)

class BranchCreateView(AuthenticatedView, CreateView):
    template_name = 'banks/branch.html'
    form_class = CreateBranchForm
    model = Branch


    def get_success_url(self):
        branch_id = self.object.id
        return ('/banks/branch/%s/details/'  % branch_id )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank_id = self.kwargs.get('bank_id')
        bank = get_object_or_404(Bank, id=bank_id)
        if self.request.user != bank.owner:
            raise PermissionDenied()
        context['bank'] = bank
        return context

    def form_valid(self, form):
        bank_id = self.kwargs.get('bank_id')
        bank = get_object_or_404(Bank, id=bank_id)
        if self.request.user != bank.owner:
            raise PermissionDenied()
        branch = form.save(commit=False)
        branch.bank = bank
        branch.save()
        return super().form_valid(form)
    
class BranchDetailsView(View):
    def get(self, request, branch_id):
        
        branch = get_object_or_404(Branch, id=branch_id)
        data = {
            "id": branch.id,
            "name": branch.name,
            "transit_num": branch.transit_num,
            "address": branch.address,
            "email": branch.email,
            "capacity": branch.capacity,
            "last_modified": branch.last_modified.isoformat()
        }
        return JsonResponse(data)


class AllBranchesView(View):
    def get(self, request, bank_id):
        bank = get_object_or_404(Bank, id=bank_id)
        branches = Branch.objects.filter(bank=bank)
        
        data = []
        for branch in branches:
            data.append({
                "id": branch.id,
                "name": branch.name,
                "transit_num": branch.transit_num,
                "address": branch.address,
                "email": branch.email,
                "capacity": branch.capacity,
                "last_modified": branch.last_modified.isoformat()
            })
        
        return JsonResponse(data, safe=False)
    

class BankListView(ListView):
    template_name = 'banks/list.html'
    queryset = Bank.objects.all()
    context_object_name = 'banks'

class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'

    def get_object(self, queryset=None):
        bank_id = self.kwargs['bank_id']
        return get_object_or_404(Bank, id=bank_id)

class BranchUpdateView(AuthenticatedView, UpdateView):
    model = Branch
    template_name = 'banks/edit_branch.html'
    fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def get_success_url(self):
        branch_id = self.kwargs['pk']
        return ('/banks/branch/%s/details/'  % branch_id )

    def get(self, request, *args, **kwargs):

        branch_id = self.kwargs['pk']
        branch = get_object_or_404(Branch, id=branch_id)
        if not self.request.user == branch.bank.owner:
            raise PermissionDenied()
        form_data = {
            'name': branch.name,
            'address': branch.address,
            'transit_num':branch.transit_num,
            'email' : branch.email,
            'capacity':branch.capacity,
        }
        form = CreateBranchForm(form_data)
        return render(request, self.template_name, {'form': form})


    def form_valid(self, form):
        # make sure the branch is owned by the user
        branch_id = self.kwargs['pk']
        branch = get_object_or_404(Branch, id=branch_id)
        if not self.request.user == branch.bank.owner:
            raise PermissionDenied()
        
        # validate the email
        email = form.cleaned_data['email']
        if email and not '@' in email:
            raise ValidationError('Enter a valid email address.')

        return super().form_valid(form)
