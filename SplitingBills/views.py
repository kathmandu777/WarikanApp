from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import FoodForm, UploadReceiptForm, WhoForm
from .models import Money, Meal

# Create your views here.

def food(request):
    ocr_from_session = request.session.get('ocr_data')
    
    print(ocr_from_session)
    FoodFormSet = formset_factory(FoodForm, extra=3)
    if request.method == 'POST':

        if 'send' in request.POST:
            formset = FoodFormSet(request.POST)

            if formset.is_valid():
                meal_cost = [0] * 5
                for form in formset:
                    food_name = form.cleaned_data.get('food_name')  # 使用しない
                    food_cost = form.cleaned_data.get('food_cost')
                    isUsedNum = 0
                    for i in range(5):
                        if form.cleaned_data.get("isUsed" + str(i + 1)):
                            isUsedNum += 1
                    for i in range(5):
                        if form.cleaned_data.get("isUsed" + str(i + 1)):
                            meal_cost[i] += food_cost / isUsedNum

                id_list = []

                # データベースへ登録
                for i in range(len(meal_cost)):
                    meal_dic = {}
                    if request.POST['food' + str(i + 1)]:
                        key = request.POST['food' + str(i + 1)]  # 料理名
                        meal_dic[key] = meal_cost[i]  # 料理の値段

                        # 登録したいモデルから最後のデータを引っ張り出す
                        last_id = Meal.objects.order_by(
                            '-pk')[:1].values()[0]['id']

                        # 新規登録したいID
                        regist_id = last_id + 1

                        # 念の為、そのIDに何も入ってないか確認
                        confirm_model = Meal.objects.filter(pk=regist_id)

                        if len(confirm_model) != 0:
                            print('登録エラー')
                        else:
                            # 登録
                            Meal.objects.create(
                                id=regist_id, meal_name=key, cost=meal_cost[i])
                            id_list.append(regist_id)

                # print(id_list)
                request.session['id_data'] = id_list
                return redirect("SplitingBills:spliting_bills_who")

            return render(request, 'food.html', {'formset': formset})
        elif 'upload' in request.POST:
            return redirect("SplitingBills:spliting_bills_upload_receipt")


    else:
        ocr_init = []
        if ocr_from_session:

            for i,name in enumerate(ocr_from_session['ocr_name']):
                cost = ocr_from_session['ocr_price'][i]
                ocr_init.append({'food_name': name, 'food_cost': cost})
        formset = FoodFormSet(initial=ocr_init)
    return render(request, 'food.html', {'formset': formset})


class UploadReceipt(generic.FormView):
    form_class = UploadReceiptForm
    template_name = 'receipt.html'

    def form_valid(self, form):
        ocr_name, ocr_price = form.ocr_func()
        ocr_data = {'ocr_name': ocr_name, 'ocr_price': ocr_price}
        self.request.session['ocr_data'] = ocr_data
        return redirect('SplitingBills:spliting_bills_food')


def who(request):
    # 人の入力フォーム
    # Moneyにも記録
    WhoFormSet = formset_factory(WhoForm, extra=3)
    id_from_session = request.session.get(
        'id_data')  # Mealオブジェクトのidリスト ex. [14,15,16]
    if id_from_session is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('SplitingBills:spliting_bills_food')

    # ヘッダーの表示
    meallist = []
    meal_obj_list = []
    for pk in id_from_session:
        meal = Meal.objects.filter(id=pk)
        if meal:
            # Mealオブジェクトのリスト [obj:47, obj:48....]
            meal_obj_list.append(meal[0])
            meallist.append(meal[0].meal_name)

    if request.method == 'POST':
        formset = WhoFormSet(request.POST)
        
        if formset.is_valid():
            
            rq = request.POST
            data_dict = {}
            
            for form in formset:
                if form.cleaned_data.get('isPaid'):
                    paid_user = form.cleaned_data.get('user_name')
                    
            

            meal_cost = [0] * len(meal_obj_list)

            # Mealよりfood_costを抜き出す ex) food_cost = [350, 100, 250]
            food_cost = []
            for obj in meal_obj_list:
                tmp = obj.cost
                food_cost.append(tmp)

            # 1人当たりの支払い金額のリスト ex) [350, 50, 125]

            for form in formset:
                
                
                for i in range(len(meal_obj_list)):
                    num_join_member = 0
                    for form in formset:
                        if form.cleaned_data.get('isJoin' + str(i + 1)):
                            num_join_member += 1
                    meal_cost[i] = food_cost[i] / num_join_member
            
            user_name_list = []
            joined_bool_list = []
            joined_list = []
            joined_meal = {}
            for form in formset:
                joined_bool_list = []
                user_name = (form.cleaned_data.get('user_name'))
                for i in range(len(meal_obj_list)):
                    if form.cleaned_data.get('isJoin' + str(i + 1)):
                        joined_bool_list.append(form.cleaned_data.get('isJoin' + str(i + 1)))
                    else:
                        joined_bool_list.append(0)
                
                user_name_list.append(user_name)
                joined_list.append(joined_bool_list)

            # {'user': ['Duser1', 'Duser2', 'Duser3'], 'joined_bool': [[True, True, 0], [True, True, True], [0, True, True]]}
            joined_meal = {'user': user_name_list, 'joined_bool': joined_list}

            
            data_dict = {'paid_user': paid_user,
                         'meal_cost': meal_cost,
                         'joined_meal': joined_meal}

            
            # アカウントが使えない代わりに、sessionに保存して遷移
            request.session['datadict'] = data_dict
            return redirect("SplitingBills:spliting_bills_result")

    formset = WhoFormSet(request.POST or None)

    context = {'formset': formset,
               'meallist': meallist}
    return render(request, 'who.html', context)

def result(request):
    data_from_session = request.session.get('datadict')
    if data_from_session is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('SplitingBills:spliting_bills_food')
    
    
    # resultdatasを作る処理
    user_cost = 0
    amount_list = []
    user_list = []
    for i, user in enumerate(data_from_session['joined_meal']['user']):
        user_cost = 0
        for j, user_bool in enumerate(data_from_session['joined_meal']['joined_bool'][i]):
            if user_bool:
                user_cost += data_from_session['meal_cost'][j]
        user_list.append(user)
        amount_list.append(user_cost)

    
    resultdatas = []
    for i, user in enumerate(user_list):
        
        if user == data_from_session['paid_user']:
            payer = user
        else:
            resultdatas.append({'user_name': user, 'amount': amount_list[i]})


    
    context = {'resultdatas':resultdatas,
               'payer': payer}
    return render(request, 'result.html', context)

def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")


def about(request):
    return render(request, "about.html")
