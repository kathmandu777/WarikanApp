from django import forms
from .models import Meal, Money


class FoodForm(forms.Form):
    food_name = forms.CharField(label="食材名")
    food_cost = forms.IntegerField(label="金額")
    
    isUsed1 = forms.BooleanField(label="使用したか", required=False)
    isUsed2 = forms.BooleanField(label="使用したか", required=False)
    isUsed3 = forms.BooleanField(label="使用したか", required=False)
    isUsed4 = forms.BooleanField(label="使用したか", required=False)
    isUsed5 = forms.BooleanField(label="使用したか", required=False)

   
