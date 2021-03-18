from django.db import models

# Create your models here.

"""
こんな感じで作っていく
class Money(models.Model):
    lender = models.ForeignKey(CustomUser, args="something")  # 貸した人
    borrower = models.ForeignKey(CustomUser, args="something")  # 借りた人
    amount = models.IntegerField()  # いくら
"""
class Food(models.Model):
    
    title = models.CharField(max_length=100) # 商品の名前
    price = models.IntegerField() # 商品の価格

    def __str__(self):
        return self.title # 表示名変更
    

class Day(models.Model):

    day = models.DateField(null=True) # 日付
    usedfood = models.ManyToManyField(Food) # その日使った食材をリンク

    def __str__(self):
        return str(self.day) # 表示名変更


class Person(models.Model):

    name = models.CharField(max_length=50)
    joined = models.ManyToManyField(Day)

    def __str__(self):
        return self.name # 表示名変更

"""
今後必要になる処理
1. Dayのusedfoodから、その日の合計金額を出す
2. Personのjoinedから、その日参加した人を取得
3. その日の１人当たりの金額を出して、その人の借りに加算
"""