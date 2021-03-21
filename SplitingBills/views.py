from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import FoodForm, UploadReceiptForm, WhoForm
from .models import Money, Meal

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
    FoodFormSet = formset_factory(FoodForm, extra=3)
    if request.method == 'POST':
        
        if 'send' in request.POST:
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
                meal_diclist = []
                

                # データベースへ登録
                for i in range(len(meal_cost)):
                    meal_dic = {}
                    if request.POST['food'+ str(i+1)]:
                        key = request.POST['food'+ str(i+1)] # 料理名
                        meal_dic[key] = meal_cost[i] # 料理の値段
                        Meal.objects.create(meal_name=key, cost=meal_cost[i])
                        meal_diclist.append(meal_dic)

                print(meal_diclist)
                return redirect("SplitingBills:spliting_bills_who")
            
            return render(request, 'food.html', {'formset': formset})

    else:
        formset = FoodFormSet()
    return render(request, 'food.html', {'formset': formset})


class UploadReceipt(generic.FormView):
    form_class = UploadReceiptForm
    template_name = 'receipt.html'

    def form_valid(self, form):
        ocr_data = form.ocr_func()
        print(ocr_data)
        return redirect('SplitingBills:spliting_bills_food')


def who(request):
    # 人の入力フォーム
    # Moneyにも記録
    meal = Meal.objects.get(id=1)
    item = {
        'name': meal.meal_name
    }

    form = WhoForm(initial=item)
    context = {'form': form}
    return render(request, 'who.html', context)


def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")


def about(request):
    return render(request, "about.html")
