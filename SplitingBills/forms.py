from django import forms
from .models import Meal, Money
 
 
class FoodForm(forms.Form):
    name = forms.CharField(label='食材')
    food = forms.CharField(label='食事')
    cost = forms.IntegerField(label='コスト')
    check1 = forms.BooleanField()
    def save(self):
        pass


FoodCreateFormSet = forms.formset_factory(FoodForm, extra=2)

"""
class FoodForm(forms.Form):
# ModelFormを継承
    class Meta():
        model = Day
        # どのmodelを利用するかmodel = モデル名で定義
        fields = ('__all__')
        # 表示するフィールド、'__all__'とすると全て
        
"""