from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import FoodForm, UploadReceiptForm, WhoForm
from .models import Money, Meal

# Create your views here.


class ResultView(generic.TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        # contextをtemplateに渡す
        # memo: contextに、ページ上で表示したいデータを渡せば良い

        context = super().get_context_data(**kwargs)

        context['from_user'] = ['rata', 'user1']
        context['to_user'] = ['user2', 'user3']
        context['user_name'] = ['user4', 'user5']
        context['amount'] = ['250', '150']
        context['money_list'] = [{'user_name': 'user1', 'amount': '250'}, {
            'user_name': 'user2', 'amount': '350'}]
        return context


def food(request):
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
                    if request.POST['food'+ str(i+1)]:
                        key = request.POST['food'+ str(i+1)] # 料理名
                        meal_dic[key] = meal_cost[i] # 料理の値段

                        # 登録したいモデルから最後のデータを引っ張り出す
                        last_id = Meal.objects.order_by('-pk')[:1].values()[0]['id']

                        # 新規登録したいID
                        regist_id = last_id + 1

                        # 念の為、そのIDに何も入ってないか確認
                        confirm_model = Meal.objects.filter( pk = regist_id )

                        if len(confirm_model) != 0:
                            print('登録エラー')
                        else:
                            # 登録
                            Meal.objects.create(id = regist_id, meal_name=key, cost=meal_cost[i])
                            id_list.append(regist_id)
                 

                
                #print(id_list)
                request.session['id_data'] = id_list
                return redirect("SplitingBills:spliting_bills_who")
            
            return render(request, 'food.html', {'formset': formset})

    else:
        formset = FoodFormSet()
    return render(request, 'food.html', {'formset': formset})


class UploadReceipt(generic.FormView):
    form_class = UploadReceiptForm
    template_name = 'receipt.html'

    def form_valid(self, form):
        ocr_data = form.ocr_func()
        print(ocr_data)
        return redirect('SplitingBills:spliting_bills_food')


def who(request):
    # 人の入力フォーム
    # Moneyにも記録
    WhoFormSet = formset_factory(WhoForm, extra=3)
    id_from_session = request.session.get('id_data') # Mealオブジェクトのidリスト ex. [14,15,16]
    if id_from_session is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('SplitingBills:spliting_bills_food')

    # ヘッダーの表示
    meallist = []
    meal_obj_list = []
    for pk in id_from_session:
        meal = Meal.objects.filter(id=pk)
        if meal:
            meal_obj_list.append(meal[0]) # Mealオブジェクトのリスト [obj:47, obj:48....]
            meallist.append(meal[0].meal_name)
    
    if request.method == 'POST':
        formset = WhoFormSet(request.POST)
        print(request.POST)
        if formset.is_valid():

            # TODO: Moneyデータベースに追加するデータをformから出す処理を書く
            rq = request.POST
            data_dict = {}
            for i in range(len(meal_obj_list)):
                if 'form-'+str(i)+'-isPaid' in rq:
                    paid_user = rq['form-'+str(i)+'-user_name']

            meal_cost = [0] * len(meal_obj_list)

            # Mealよりfood_costを抜き出す ex) food_cost = [350, 100, 250]
            food_cost = []
            for obj in meal_obj_list:
                    tmp = obj.cost
                    food_cost.append(tmp)
            
            
            # TODO: ここからです よろしくお願いします
            # 1人当たりの支払い金額のリストがほしいです ex) [350, 50, 125]
            
            for form in formset:
                print('reset')
                is_join_num = 0
                for i in range(len(meal_obj_list)):
                    if form.cleaned_data.get("isJoin" + str(i + 1)):
                        is_join_num += 1 # 縦の個数カウント
                        
                        
                
                
            print(meal_cost)






            
            """ モデルに追加する処理　アカウントがないので使わない
            # 登録したいモデルから最後のデータを引っ張り出す
            last_id = Money.objects.order_by('-pk')[:1].values()[0]['id']
            # 新規登録したいID
            regist_id = last_id + 1
            # 念の為、そのIDに何も入ってないか確認
            confirm_model = Money.objects.filter( pk = regist_id )

            if len(confirm_model) != 0:
                print('登録エラー')
            else:
                # 登録


                #Money.objects.create(meal = MealObject ,)
                id_list = []
                id_list.append(regist_id)"""

            # アカウントが使えない代わりに、sessionに保存して遷移
            request.session['datas'] = data_dict
            #return redirect("SplitingBills:spliting_bills_who")
    
    formset = WhoFormSet(request.POST)
        
    context = {'formset': formset,
               'meallist': meallist}
    return render(request, 'who.html', context)


def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")


def about(request):
    return render(request, "about.html")
