from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import FoodForm
from .models import Money

# Create your views here.


class ResultView(generic.TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        # contextをtemplateに渡す
        # memo: contextに、ページ上で表示したいデータを渡せば良い

        context = super().get_context_data(**kwargs)

        context['from_user'] = ['rata', 'user1']
        context['to_user'] = ['user2', 'user3']
        context['user_name'] = ['user4', 'user5']
        context['amount'] = ['250', '150']
        context['money_list'] = [{'user_name': 'user1', 'amount': '250'}, {
            'user_name': 'user2', 'amount': '350'}]
        return context


def food(request):
    
    
    if request.method == 'POST':

        new_initial = []
        
        
        
        count = 0
        
        for post in request.POST:
            if str(post).endswith('food_name'):
                
                if request.POST['form-'+str(count)+'-' + 'food_name']:
                    new_initial.append({'food_name': request.POST['form-'+str(count)+'-'+'food_name'],
                                        'food_cost': request.POST['form-'+str(count)+'-'+'food_cost'],
                                        })
                    
                    
                count += 1
                
        if 'increase' in request.POST:
            FoodFormSet = formset_factory(FoodForm, extra=1)
            formset = FoodFormSet(initial=new_initial)
            return render(request, 'food.html', {'formset': formset})
        
        if 'send' in request.POST:
            FoodFormSet = formset_factory(FoodForm, extra=0)
            formset = FoodFormSet(request.POST)
            
            if formset.is_valid():
                
                meal_cost = [0] * 5
                for form in formset:
                    food_name = form.cleaned_data.get('food_name')  # 使用しない
                    food_cost = form.cleaned_data.get('food_cost')
                    isUsedNum = 0
                    for i in range(5):
                        if form.cleaned_data.get("isUsed" + str(i + 1)):
                            isUsedNum += 1
                    for i in range(5):
                        if form.cleaned_data.get("isUsed" + str(i + 1)):
                            meal_cost[i] += food_cost / isUsedNum
                print(meal_cost)
                # return reverse_lazy("SplitingBills:spliting_bills_who")
            
            return render(request, 'food.html', {'formset': formset})

    else:
        FoodFormSet = formset_factory(FoodForm, extra=3)
        formset = FoodFormSet()
        
    return render(request, 'food.html', {'formset': formset})


def who(request):
    # 人の入力フォーム
    # Moneyにも記録
    return HttpResponse('This is who page.')


def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")


def about(request):
    return render(request, "about.html")
