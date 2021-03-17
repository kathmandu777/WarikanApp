from django.db import models

# Create your models here.

"""
こんな感じで作っていく
class Money(models.Model):
    lender = models.ForeignKey(CustomUser, args="something")  # 貸した人
    borrower = models.ForeignKey(CustomUser, args="something")  # 借りた人
    amount = models.IntegerField()  # いくら
"""
