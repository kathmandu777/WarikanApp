from django.shortcuts import render
from django.views.generic import TemplateView

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
        context['price'] = ['250', '150']
        return context

def food(request):
    # Mealの入力フォーム
    return HttpResponse('This is food page.')


def who(request):
    # 人の入力フォーム
    # Moneyにも記録
    return HttpResponse('This is who page.')

def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")
