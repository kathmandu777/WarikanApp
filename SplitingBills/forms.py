from django import forms
from .models import Meal, Money
import os
import io
from django.core.validators import FileExtensionValidator
# 絶対パス必ず
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"絶対パスでjsonのある場所を指定"
from google.cloud import vision


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
    receipt = forms.ImageField(label="レシート", validators=[
                               FileExtensionValidator(['png', 'jpg'])])

    def ocr_func(self):
        receipt = self.cleaned_data['receipt'].read()
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=receipt)
        response = client.document_text_detection(image=image)

        def get_sorted_lines(response):
            document = response.full_text_annotation
            bounds = []
            for page in document.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                x = symbol.bounding_box.vertices[0].x
                                y = symbol.bounding_box.vertices[0].y
                                text = symbol.text
                                bounds.append(
                                    [x, y, text, symbol.bounding_box])
            bounds.sort(key=lambda x: x[1])
            old_y = -1
            line = []
            lines = []
            threshold = 1
            for bound in bounds:
                x = bound[0]
                y = bound[1]
                if old_y == -1:
                    old_y = y
                elif old_y - threshold <= y <= old_y + threshold:
                    old_y = y
                else:
                    old_y = -1
                    line.sort(key=lambda x: x[0])
                    lines.append(line)
                    line = []
                line.append(bound)
            line.sort(key=lambda x: x[0])
            lines.append(line)
            return lines
        lines = get_sorted_lines(response)
        name_list = []
        price_list = []
        food_name = ""
        food_price = ""
        check_point = 0
        for line in lines:
            texts = [i[2] for i in line]

            for i in range(len(texts)):

                if texts[i] != chr(165) and check_point == 0:
                    food_name += texts[i]
                elif texts[i] == chr(165):
                    check_point = 1
                else:
                    food_price += texts[i]
            check_point = 0
            name_list.append(food_name)
            price_list.append(food_price)
            food_name = ""
            food_price = ""

        name_list = [a for a in name_list if a != '']
        price_list = [a for a in price_list if a != '']
        print(name_list)
        print(price_list)
        return name_list


class WhoForm(forms.Form):

    user_name = forms.CharField(required=False)
    isPaid = forms.BooleanField(required=False)
    isJoin1 = forms.BooleanField(required=False)
    isJoin2 = forms.BooleanField(required=False)
    isJoin3 = forms.BooleanField(required=False)
    isJoin4 = forms.BooleanField(required=False)
    isJoin5 = forms.BooleanField(required=False)
 
   
 
    
