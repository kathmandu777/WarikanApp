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
    cost = models.PositiveSmallIntegerField(verbose_name='価格')
    participant = models.ManyToManyField(CustomUser, verbose_name='参加者(複数)')
    meal_name = models.CharField(max_length=50, verbose_name='料理名')
    payer = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                              null=True, verbose_name='購入者', related_name='Meal_payer')

    # 管理画面などで表示される文字列を定義
    def __str__(self):
        return str(self.id) + self.meal_name  # 表示名変更


class Money(models.Model):
    meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, verbose_name='どの食事についてか')
    amount = models.IntegerField(verbose_name='金額')
    lender = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               null=True, verbose_name='貸した人', related_name='Money_lender')
    borrower = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 null=True, verbose_name='借りた人', related_name='Money_borrower')  # 借りた人
    is_Done = models.BooleanField(verbose_name='支払われたかどうか')

    def __str__(self):
        return str(self.meal)