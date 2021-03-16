from django.urls import path
from . import views

app_name = 'SplitingBills'
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', undefined, name='about'),  # アプリ概要

    """割り勘(ログイン状態かどうかでUIを変える必要あり)"""
    # 食材入力
    path('spliting-bills-food', undefined, name='spliting_bills_food'),
    # 誰と食事をしたかを入力
    path('spliting-bills-who', undefined, name='spliting_bills_who'),
    # 1人あたりの支払い金額
    path('spliting-bills-result/', undefined, name='spliting_bills_result'),

    """ユーザーがログインしているときのみ"""
    # 今までに作った料理の記録
    path('history/', undefined, name='history'),
    # 貸し一覧(他人にお金を払ってもらっていない状態)
    path('loan-list/', undefined, name='loan_list'),
    # 借り一覧(他人にお金を払ってない状態)
    path('borrowed-list/', undefined, name='borrowed_list'),
]
