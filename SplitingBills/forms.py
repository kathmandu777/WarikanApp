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

    def save(self):
        pass


class UploadReceiptForm(forms.Form):
    receipt = forms.ImageField(label="レシート")

    def ocr_func(self):
        receipt = self.cleaned_data['receipt']
        print(receipt)
        # TODO:OCRの処理（以下の形式は例。どんな形でも大丈夫）
        return [{"name": "milk", "cost": 150}, {"name": "banana", "cost": 200}]
