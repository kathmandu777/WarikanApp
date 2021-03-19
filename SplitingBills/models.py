from django.db import models
from accounts.models import CustomUser
# Create your models here.

"""
こんな感じで作っていく
class Money(models.Model):
    lender = models.ForeignKey(CustomUser, args="something")  # 貸した人
    borrower = models.ForeignKey(CustomUser, args="something")  # 借りた人
    amount = models.IntegerField()  # いくら
"""


class Meal(models.Model):
    when = models.DateField(null=True, verbose_name='日付')
    cost = models.IntegerField(verbose_name='価格')
    participant = models.ManyToManyField(CustomUser, verbose_name='参加者(複数)')
    meal_name = models.CharField(max_length=50, verbose_name='食事名')
    # idは自動でつけられる
    payer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, verbose_name='購入者', related_name='Meal_payer')
    

    def __str__(self):
        return self.meal_name # 表示名変更


class Money(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT,verbose_name='どの食事についてか')
    amount = models.IntegerField(verbose_name='金額')
    lender = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, verbose_name='貸した人', related_name='Money_lender')
    borrower = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, verbose_name='借りた人', related_name='Money_borrower')  # 借りた人
    is_Done = models.BooleanField(verbose_name='支払われたかどうか')
    
    def __str__(self):
        return str(self.meal)

""" old ver
class Day(models.Model):

    day = models.DateField(null=True, verbose_name='日付') # 日付
    
    def __str__(self):
        return str(self.day) # 表示名変更


class Person(models.Model):

    name = models.CharField(max_length=50, verbose_name='名前')
    joined = models.ManyToManyField(Day, verbose_name='食事に参加した日') # 食事に参加した日をマーク
    
    def __str__(self):
        return self.name # 表示名変更


class Food(models.Model):
    
    title = models.CharField(max_length=100, verbose_name='食材') # 商品の名前
    price = models.IntegerField(verbose_name='価格') # 商品の価格
    pay = models.ForeignKey(Person, on_delete=models.PROTECT, null=True, verbose_name='購入した人') # 食材を購入した人
    usedday = models.ManyToManyField(Day, verbose_name='使った日') # 食材を使った日

    def __str__(self):
        return self.title # 表示名変更
"""

"""
1. Foodのuseddayから、その日の合計金額を出す
2. Personのjoinedから、その日参加した人を取得
3. その日の１人当たりの金額を出して、その人の借りに加算
"""