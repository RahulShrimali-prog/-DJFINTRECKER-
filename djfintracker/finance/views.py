from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from finance.form import registerForm, Transactionform, Goalform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from.models import Transaction,Goal
from django.db.models import Sum
from .admin import transactionsresournce
from django.contrib import messages


# Create your views here.

class registerView(View):
    def get(self, request, *args, **kwargs):
        form = registerForm()
        return render(request, 'finance/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'Account Created Successfully !')
            return redirect('dashboard')
        return render(request, 'finance/register.html', {'form': form})


class dashboardview(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transaction = Transaction.objects.filter(user= request.user)
        goals = Goal.objects.filter(user= request.user)
    #Calculate total income and expance
        total_income=Transaction.objects.filter(user= request.user, transaction_type='income') .aggregate(Sum('amount'))['amount__sum'] or 0

        total_expense=Transaction.objects.filter(user= request.user,transaction_type='expense') .aggregate(Sum('amount'))['amount__sum'] or 0

        net_savings = total_income - total_expense
        
        remaining_savings = net_savings
        goal_progress = []
        for goal in goals:
            if remaining_savings >= goal.target_amount:
                goal_progress.append({'goal':goal,'progress':100})
                remaining_savings -=goal.target_amount
            elif remaining_savings > 0:
                progress =(remaining_savings / goal.target_amount) * 100
                goal_progress.append({'goal':goal,'progress':progress})
                remaining_savings = 0
            else:
                goal_progress.append({'goal':goal,'progress':0})

        context = {
            'transaction':transaction,
            'total_income':total_income,
            'total_expense':total_expense,
            'net_savings': net_savings,
            'goal_progress':goal_progress,
        }
        return render(request, 'finance/dashboard.html', context)
    
class TransectioncreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form= Transactionform()
        return render(request, 'finance/Transaction_form.html' , {'form': form})
    def post(self, request, *args, **kwargs):
        form = Transactionform(request.POST)
        if form.is_valid():
            Transaction= form.save(commit=False)
            Transaction.user=request.user
            Transaction.save()
            messages.success(request,'Transaction Added Successfully !')
            return redirect('dashboard')
        return render(request, 'finance/Transaction_form.html' , {'form': form})

class Transactionlistview(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
       transactions = Transaction.objects.filter(user = request.user)
       return render(request, 'finance/Transaction_list.html' , {'transactions':transactions})
    
class GoalView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form= Goalform()
        return render(request, 'finance/Goal_form.html' , {'form': form})
    def post(self, request, *args, **kwargs):
        form = Goalform(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request,'Goal Created Successfully !')
            return redirect('dashboard')
        return render(request, 'finance/Goal_form.html' , {'form': form})
    
# Make sure to import Transactionsresournce at the top if it's defined elsewhere, e.g.:
# from .resources import Transactionsresournce

def export_transactions(request):
    user_transactions = Transaction.objects.filter(user= request.user)

    # Replace with the correct class name if it's a typo, e.g. TransactionsResource
    transactions_resource = transactionsresournce()
    dataset = transactions_resource.export(queryset= user_transactions)

    excel_data = dataset.export('xlsx')
    messages.success(request, 'Downloaded Successfully!')

# create an HttpResponce with the correct MIME type for an Excel file
    response =  HttpResponse(excel_data, content_type= 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Set a header for downloding the file 
    response['content-Disposition'] = 'attachment; filename=transactions_report.xlsx'
    return response
    