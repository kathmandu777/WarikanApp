from django import forms
from .models import Meal, Money
 
 
class FoodForm(forms.Form):
    test = forms.CharField()
    def save(self):
        pass
"""
class FoodForm(forms.Form):
# ModelFormを継承
    class Meta():
        model = Day
        # どのmodelを利用するかmodel = モデル名で定義
        fields = ('__all__')
        # 表示するフィールド、'__all__'とすると全て
        
"""