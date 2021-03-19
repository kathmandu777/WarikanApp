from django.urls import path
from . import views
from .views import ResultView
app_name = 'SplitingBills'
urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', undefined(修正必須), name='about'),  # アプリ概要
    path('terms-of-service', views.terms_of_service,
         name='terms_of_service'),  # 利用規約

    #### 割り勘(ログイン状態かどうかでUIを変える必要あり) ####
    # 食材入力
    path('spliting-bills-food/', views.food, name='spliting_bills_food'),
    # 誰と食事をしたかを入力
    path('spliting-bills-who/', views.who, name='spliting_bills_who'),
    # 1人あたりの支払い金額
    path('spliting-bills-result/', ResultView.as_view(), name='spliting_bills_result'),

    #### ユーザーがログインしているときのみ #####
    # 今までに作った料理の記録
    # path('history/', undefined(修正必須), name='history'),
    # 貸し一覧(他人にお金を払ってもらっていない状態)
    # path('loan-list/', undefined(修正必須), name='loan_list'),
    # 借り一覧(他人にお金を払ってない状態)
    # path('borrowed-list/', undefined(修正必須), name='borrowed_list'),
]
