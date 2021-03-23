from django.shortcuts import render
from django.http import FileResponse
import random
from . import method
from .models import Test

count = 0

#スタート画面
def index(request):
    return render(request, 'menu/start.html')

#主菜ランダム表示
def start(request):
    params = method.main_random()
    return render(request, 'menu/index.html', params)

#主菜決定画面（献立提案ボタンの表示）
def next(request):
    main_num = list(request.POST.values())[1]
    params = method.next_choice(main_num)
    return render(request, 'menu/next.html', params)

#レシピの組み合わせを予測
def predict(request):
    global count

    #主菜のインデックスで副菜と汁物を予想
    main_num = request.POST['main_num']

    #ユーザーがログインしているかどうか
    if request.user.username:
        user_name = request.user.username
        if Test.objects.filter(name=user_name).last():
            method.make_train(main_num)
            params = method.user_model_predict(user_name)
        else:
            method.make_train(main_num)
            params = method.menu_predict(main_num)   
    else:
        method.make_train(main_num)
        params = method.menu_predict(main_num)

    #副菜と汁物のリストを取得
    sub_name_list = params['sub_name_list']
    soup_name_list = params['soup_name_list']
    #レシピ情報の取得
    recipe_info = method.recipe_info(main_num, sub_name_list, soup_name_list, count)
    params.update(recipe_info)
    #sub_num,soup_numの取得
    sub_num = params['sub_num']
    soup_num = params['soup_num']


    #ユーザーがログインしているかどうか
    if request.user.username:
        user_name = request.user.username
        user_mail = request.user.email
    else:
        user_name = 'ゲスト'
        user_mail = 'None'

    #予測した組み合わせの登録
    test = Test(name=user_name, mail=user_mail, sub_list=sub_name_list, soup_list=soup_name_list,
                 mainNum=main_num, subNum=sub_num, soupNum=soup_num, judge=True)
    test.save()

    print('soup_name', params['soup_name'])

    #汁物ありとなしで表示の切り替え
    if params['soup_name'] != 'なし':
        return render(request, 'menu/result.html', params)
    elif params['soup_name'] == 'なし':
        return render(request, 'menu/result_nosoup.html', params)


#他の組み合わせの表示
def next_predict(request):
    global count

    #ユーザーがログインしているかどうか
    if request.user.username:
        user_name = request.user.username
        user_mail = request.user.email
    else:
        user_name = 'ゲスト'
        user_mail = 'None'

    #組み合わせの判定にFalseを設定
    notChoice_id = Test.objects.filter(name=user_name).last().id
    obj = Test.objects.get(id=notChoice_id)
    obj.judge = False
    obj.save()

    #保存したモデルの情報を取得
    sub_name_list = Test.objects.filter(name=user_name).values('sub_list').last()
    sub_name_list = sub_name_list['sub_list'].replace("[", '').replace("]", '').split(', ')
    sub_name_list = [int(s) for s in sub_name_list]
    soup_name_list = Test.objects.filter(name=user_name).values('soup_list').last()
    soup_name_list = soup_name_list['soup_list'].replace("[", '').replace("]", '').split(', ')
    soup_name_list = [float(s) for s in soup_name_list]


    #予測した組み合わせの次のデータを取得
    count += 1
    if count >= len(sub_name_list) or count >= len(soup_name_list):
        count = 0
    params = method.recipe_info(request.POST['main_num'], sub_name_list, soup_name_list, count)

    #新しい組み合わせの保存
    main_num = params['main_num']
    sub_num = params['sub_num']
    soup_num = params['soup_num']
    test = Test(name=user_name, mail=user_mail, sub_list=sub_name_list, soup_list=soup_name_list,
                 mainNum=main_num, subNum=sub_num, soupNum=soup_num, judge=True)
    test.save()

    #汁物がありかなしで表示の切り替え
    if params['soup_name'] != 'なし':
        return render(request, 'menu/result.html', params)
    elif params['soup_name'] == 'なし':
        return render(request, 'menu/result_nosoup.html', params)


#決定したモデルの表示
def decision(request):
    #ログインしているかどうか
    if request.user.username:
        user_name = request.user.username
    else:
        user_name = 'ゲスト'

    #決定したモデルの情報を取得
    main_num = Test.objects.filter(name=user_name).values('mainNum').last()
    main_num = main_num['mainNum']
    sub_name_list = Test.objects.filter(name=user_name).values('sub_list').last()
    sub_name_list = sub_name_list['sub_list'].replace("[", '').replace("]", '').split(', ')
    sub_name_list = [int(s) for s in sub_name_list]
    soup_name_list = Test.objects.filter(name=user_name).values('soup_list').last()
    soup_name_list = soup_name_list['soup_list'].replace("[", '').replace("]", '').split(', ')
    soup_name_list = [float(s) for s in soup_name_list]
    decision_count = request.POST['count']
    params = method.recipe_info(main_num, sub_name_list, soup_name_list, decision_count)

    #組み合わせの判定にTrueを設定
    okChoice_id = Test.objects.filter(name=user_name).last().id
    obj = Test.objects.get(id=okChoice_id)
    obj.judge = True
    obj.save()

    #汁物がありかなしか
    if params['soup_name'] != 'なし':
        return render(request, 'menu/decision.html', params)
    elif params['soup_name'] == 'なし':
        return render(request, 'menu/decision_nosoup.html', params)



#ローディング表示
def loading(request):
    main_num = list(request.POST.values())[1]
    params = method.next_choice(main_num)
    return render(request, 'menu/loading.html', params)



#認証関係のモジュール
from .forms import SignUpForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

#登録処理
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()

    params = {
        'form': form
    }
    return render(request, 'menu/signup.html', params)

#ログイン処理
def login(request):
    return render(request, 'menu/login.html')
