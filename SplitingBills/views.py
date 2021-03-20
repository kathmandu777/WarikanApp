from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import FoodForm

from .models import Money

# Create your views here.
from django.http import HttpResponse


class ResultView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        # contextをtemplateに渡す
        # memo: contextに、ページ上で表示したいデータを渡せば良い
        
        context = super().get_context_data(**kwargs)
        
        context['from_user'] = ['rata', 'user1']
        context['to_user'] = ['user2', 'user3'] 
        context['user_name'] = ['user4', 'user5']
        context['amount'] = ['250', '150']
        context['money_list'] = [{'user_name': 'user1', 'amount': '250'},{'user_name': 'user2', 'amount': '350'}]
        return context

def food(request):
    # Mealの入力フォーム
    if request.method == 'POST':
        form = FoodForm(request.POST)
        """
        if form.is_valid():
            form.save()
            return redirect('who')
        """
    else:
        form = FoodForm()
    
    return render(request, 'food.html', {'form': form})


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
