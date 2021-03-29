import numpy as np
import pandas as pd
import random
import csv
import fcntl
import shutil
import pickle
import lightgbm as lgb
from . import features
from .models import Test
import time


with open('rakuten_main.csv') as f:
    reader = csv.DictReader(f)
    main = [row for row in reader]

with open('rakuten_sub.csv') as f:
    reader = csv.DictReader(f)
    sub = [row for row in reader]

with open('rakuten_soup.csv') as f:
    reader = csv.DictReader(f)
    soup = [row for row in reader]

with open("menu_ai.pickle", mode="rb") as f:
    model = pickle.load(f)

#汁物を必要としないリスト
not_soup_list = ['鍋', 'ラーメン', 'うどん', '蕎麦', '素麺', 'ハヤシライス',
                'つけ麺', 'おでん', 'クリームシチュー', 'ビーフシチュー',
                '坦々麺', '冷麺', 'ちゃんぽん', 'スープカレー']


#主菜をランダムに表示
def main_random():
    main_num_1 = random.randint(0, len(main)-1)
    main_num_2 = random.randint(0, len(main)-1)
    main_num_3 = random.randint(0, len(main)-1)
    main_num_4 = random.randint(0, len(main)-1)
    main_num_5 = random.randint(0, len(main)-1)
    main_num_6 = random.randint(0, len(main)-1)
    main_num_7 = random.randint(0, len(main)-1)
    main_num_8 = random.randint(0, len(main)-1)
    main_num_9 = random.randint(0, len(main)-1)

    params = {
        'main_num_1': main_num_1,
        'main_num_2': main_num_2,
        'main_num_3': main_num_3,
        'main_num_4': main_num_4,
        'main_num_5': main_num_5,
        'main_num_6': main_num_6,
        'main_num_7': main_num_7,
        'main_num_8': main_num_8,
        'main_num_9': main_num_9,

        'main_image_1': main[main_num_1]['foodImageUrl'],
        'main_image_2': main[main_num_2]['foodImageUrl'],
        'main_image_3': main[main_num_3]['foodImageUrl'],
        'main_image_4': main[main_num_4]['foodImageUrl'],
        'main_image_5': main[main_num_5]['foodImageUrl'],
        'main_image_6': main[main_num_6]['foodImageUrl'],
        'main_image_7': main[main_num_7]['foodImageUrl'],
        'main_image_8': main[main_num_8]['foodImageUrl'],
        'main_image_9': main[main_num_9]['foodImageUrl'],

        'main_name_1': main[main_num_1]['recipeTitle'],
        'main_name_2': main[main_num_2]['recipeTitle'],
        'main_name_3': main[main_num_3]['recipeTitle'],
        'main_name_4': main[main_num_4]['recipeTitle'],
        'main_name_5': main[main_num_5]['recipeTitle'],
        'main_name_6': main[main_num_6]['recipeTitle'],
        'main_name_7': main[main_num_7]['recipeTitle'],
        'main_name_8': main[main_num_8]['recipeTitle'],
        'main_name_9': main[main_num_9]['recipeTitle'],

        'main_description_1': main[main_num_1]['recipeDescription'],
        'main_description_2': main[main_num_2]['recipeDescription'],
        'main_description_3': main[main_num_3]['recipeDescription'],
        'main_description_4': main[main_num_4]['recipeDescription'],
        'main_description_5': main[main_num_5]['recipeDescription'],
        'main_description_6': main[main_num_6]['recipeDescription'],
        'main_description_7': main[main_num_7]['recipeDescription'],
        'main_description_8': main[main_num_8]['recipeDescription'],
        'main_description_9': main[main_num_9]['recipeDescription'],
    }
    return params

#選んだ主菜を表示
def next_choice(main_num):
    main_image = main[int(main_num)]['foodImageUrl']
    main_name = main[int(main_num)]['recipeTitle']
    main_description = main[int(main_num)]['recipeDescription']

    params = {
        'main_num': main_num,
        'main_image': main_image,
        'main_name': main_name,
        'main_description': main_description,
    }
    return params

#レシピの組み合わせを予測
def make_train(main_num):
    main_num = int(main_num)
    sub_num_list = []
    soup_num_list = []
    soup_num = 0

    #空のファイルをコピーしてtrain.csvを初期化
    shutil.copyfile("empty.csv", "train.csv")

    #鍋や麺類の場合は汁物をなしにする
    for not_soup in not_soup_list:
        if not_soup in main[main_num]['recipeTitle']:
            soup_num = len(soup) - 1

    #train.csvを開いてロックする
    with open('train.csv', 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        reader = csv.reader(f)
        train = [row for row in reader]
        train_writer = csv.writer(f, lineterminator='\n')

        #副菜と汁物のランダムな組み合わせを取得
        for i in range(500):
            #ランダムな組み合わせのデータ1列を作る
            #combi = 1行のみで全て0
            with open('combi.csv') as ff:
                reader = csv.DictReader(ff)
                combi = [row for row in reader]

            #副菜をランダムに選ぶ
            sub_num = random.randint(0, len(sub)-1)
            #汁物をランダムに選ぶ(汁物無しでなければ)
            if soup_num != (len(soup)-1):
                soup_num = random.randint(0, len(soup)-2)

            #主菜、副菜、汁物、主菜IDを入力
            combi[0]['主菜'] = main[main_num]['recipeTitle']
            combi[0]['副菜'] = sub[sub_num]['recipeTitle']
            combi[0]['汁物'] = soup[soup_num]['recipeTitle']
            combi[0]['主菜ID'] = main[main_num]['recipeId']

            #材料のリストの作成
            all_list = list(combi[0].keys())[7:]
            
            #レシピ情報に材料リストの物を含んでいれば1を入力
            for material in all_list:
                if material in main[main_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in sub[sub_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in soup[soup_num]['recipeMaterial']:
                    combi[0][material] = 1  

            #ジャンルの入力
            combi[0]['main_genre'] = main[main_num]['genre']
            combi[0]['sub_genre'] = sub[sub_num]['genre']
            combi[0]['soup_genre'] = soup[soup_num]['genre']

            #作成した1列のデータをtrain.csvに追加する
            train_writer.writerow(combi[0].values())

        #train.csvのロックを解除
        f.flush()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def menu_predict(main_num):
    main_num = int(main_num)
    #train.csvをpandasで読み込む
    train = pd.read_csv('train.csv', index_col=0)
    sub_df = pd.read_csv('rakuten_sub.csv', index_col=0)      
    soup_df = pd.read_csv('rakuten_soup.csv', index_col=0)    
    train.reset_index(drop=True, inplace=True)

    #main_genreのonehot
    add_columns = pd.DataFrame(np.zeros(4).reshape(1, 4), columns=['main_genre_1', 'main_genre_2', 'main_genre_3', 'main_genre_4'])
    for add_col in add_columns:
        train[add_col] = 0
    train.drop('main_genre', axis=1, inplace=True)
    main_genre_get = 'main_genre_' + main[main_num]['genre']
    train[main_genre_get] = 1
    
    #sub_genreのonehot
    train = pd.get_dummies(train, columns=['sub_genre'])

    #soup_genreのonehot
    #データの中に汁なしがあるかどうか
    if 0 not in train['soup_genre']:
        train = pd.get_dummies(train, columns=['soup_genre'])
    elif 0 in train['soup_genre']:
        train['soup_genre_0'] = 1 
        train[['soup_genre_1', 'soup_genre_2', 'soup_genre_3', 'soup_genre_4']] = 0
        train.drop('soup_genre', axis=1, inplace=True)

    #主菜、副菜、汁物のジャンル(和、洋、中、その他)ごとのトータル
    train['genre_total_1'] = train['main_genre_1'] + train['sub_genre_1'] + train['soup_genre_1']
    train['genre_total_2'] = train['main_genre_2'] + train['sub_genre_2'] + train['soup_genre_2']
    train['genre_total_3'] = train['main_genre_3'] + train['sub_genre_3'] + train['soup_genre_3']
    train['genre_total_4'] = train['main_genre_4'] + train['sub_genre_4'] + train['soup_genre_4']

    #元データを残しておく
    train_origin = train.copy(deep=True)

    #特徴量の追加
    train = features.features(train)

    train.drop(['ID', '主菜', '副菜', '汁物', '主菜ID', '採用/不採用'], axis=1, inplace=True)

    #モデルを使って予想
    pred = model.predict_proba(train)
    #予測上位順に並び替え、インデックスを取得
    pred_sort_index = np.argsort(pred[:, 0])

    #コピーしておいた元データから上位50件の副菜、汁物の名前リストを作成
    sub_name_list = []
    soup_name_list = []
    for i in range(50):
        #予測した副菜のリスト作成
        sub_name = train_origin.iloc[pred_sort_index[i]]['副菜']
        sub_name = sub_df[sub_df['recipeTitle']==sub_name]['recipeId'].values[0]  
        sub_name_list.append(sub_name)
        #副菜重複削除
        sub_name_list = sorted(set(sub_name_list), key=sub_name_list.index)

        #予測した汁物のリスト作成
        soup_name = train_origin.iloc[pred_sort_index[i]]['汁物']
        soup_name = soup_df[soup_df['recipeTitle']==soup_name]['recipeId'].values[0]    
        soup_name_list.append(soup_name)
        #汁物重複削除
        if soup_name_list[0] != 0:     #if soup_name_list[0] !='なし':
            soup_name_list = sorted(set(soup_name_list), key=soup_name_list.index)

    params = {
        'main_num': main_num,
        'sub_name_list': sub_name_list,
        'soup_name_list': soup_name_list,
    }
    return params

#予測したレシピの情報を表示
def recipe_info(main_num, sub_name_list, soup_name_list, count):
    #main_numをstr型からint型へ変換
    main_num = int(main_num)
    count = int(count)

    #主菜情報
    main_image = main[main_num]['foodImageUrl']
    main_name = main[main_num]['recipeTitle']
    main_description = main[main_num]['recipeDescription']
    main_url = main[main_num]['recipeUrl']

    #副菜情報
    for i in range(len(sub)):
        if int(sub[i]['recipeId']) == sub_name_list[count]:   
            sub_num = i
            sub_name = sub[i]['recipeTitle']
            sub_image = sub[i]['foodImageUrl']
            sub_description = sub[i]['recipeDescription']
            sub_url = sub[i]['recipeUrl']

    #汁物情報
    for i in range(len(soup)-1):
        if float(soup[i]['recipeId']) == soup_name_list[count]:    
            soup_num = i
            soup_name = soup[i]['recipeTitle']
            soup_image = soup[i]['foodImageUrl']
            soup_description = soup[i]['recipeDescription']
            soup_url = soup[i]['recipeUrl']

    params = {
        'main_num': main_num,
        'main_image': main_image,
        'main_name': main_name,
        'main_description': main_description,
        'main_url': main_url,
        'sub_num': sub_num,
        'sub_name': sub_name,
        'sub_image': sub_image,
        'sub_description': sub_description,
        'sub_url': sub_url,
        'soup_num': soup_num,
        'soup_name': soup_name,
        'soup_image': soup_image,
        'soup_description': soup_description,
        'soup_url': soup_url,
        'count': count,
    }
    return params




######################################################################################################
######################                   ユーザー別の処理                    ############################
######################################################################################################

#ユーザー別モデルの作成
def model_make(train):
    t_1 = time.time()
    #2値化
    columns = list(train.columns[6:-3])
    for column in columns:
        train[column] = train[column].map(lambda x: 1 if x >=1 else 0)
    print('二値化', time.time() - t_1)

    #特徴量の追加
    #train = features.features(train)
    #print('特徴量の追加', time.time() - t_1)

    #リセットインデックス
    train.reset_index(drop=True, inplace=True)
    train['soup_genre'] = train['soup_genre'].astype(int)

    #ワンホットエンコーディング
    train = pd.get_dummies(train, columns=['main_genre', 'sub_genre', 'soup_genre'])
    print('ワンホットエンコーディング', time.time() - t_1)

    #ジャンルトータルの作成
    train['genre_total_1'] = train['main_genre_1'] + train['sub_genre_1'] + train['soup_genre_1']
    train['genre_total_2'] = train['main_genre_2'] + train['sub_genre_2'] + train['soup_genre_2']
    train['genre_total_3'] = train['main_genre_3'] + train['sub_genre_3'] + train['soup_genre_3']
    train['genre_total_4'] = train['main_genre_4'] + train['sub_genre_4'] + train['soup_genre_4']

    train.drop(['ID', '主菜', '副菜', '汁物', '主菜ID'], axis=1, inplace=True)

    #説明変数と目的変数の分割
    x = train.drop('採用/不採用', axis=1)
    y = train['採用/不採用']

    #モデルの作成
    user_model = lgb.LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=1.0,
               importance_type='split', learning_rate=0.08, max_depth=6,
               min_child_samples=23, min_child_weight=0.001, min_split_gain=0,
               n_estimators=130, n_jobs=-1, num_leaves=30, objective='binary',
               random_state=None, reg_alpha=0.0, reg_lambda=0.0, silent=True,
               subsample=1.0, subsample_for_bin=20000, subsample_freq=0)
    user_model.fit(x, y)

    print('モデル作成', time.time() - t_1)
    return user_model



#######################################################################################################

#ユーザーモデルで予測する
def user_model_predict(user_name):

    #元データをコピーしておく
    shutil.copyfile("train_model.csv", "train_model_origin.csv")
    
    #ユーザーデータをプラスしてモデルを作成
    with open('train_model.csv', 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        reader = csv.reader(f)
        train_model = [row for row in reader]
        train_model_writer = csv.writer(f, lineterminator='\n')

        #combi = 1行のみで全て0
        with open('combi.csv') as ff:
            reader = csv.DictReader(ff)
            combi = [row for row in reader]
    
        #ユーザーネームからユーザーのデータを取り出す
        data_list = Test.objects.filter(name=user_name).values('mainNum', 'subNum', 'soupNum', 'judge')

        #ユーザーのモデルを1行づつ追加
        for data in data_list:
            main_num = data['mainNum']
            sub_num = data['subNum']
            soup_num = data['soupNum']
            judge = data['judge']

            #主菜、副菜、汁物、主菜IDを入力
            combi[0]['主菜'] = main[main_num]['recipeTitle']
            combi[0]['副菜'] = sub[sub_num]['recipeTitle']
            combi[0]['汁物'] = soup[soup_num]['recipeTitle']
            combi[0]['主菜ID'] = main[main_num]['recipeId']

            if judge:
                combi[0]['採用/不採用'] = 1.0
            elif not judge:
                combi[0]['採用/不採用'] = 0.0

            #材料のリストの作成
            all_list = list(combi[0].keys())[7:]
            
            #レシピ情報に材料リストの物を含んでいれば1を入力
            for material in all_list:
                if material in main[main_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in sub[sub_num]['recipeMaterial']:
                    combi[0][material] = 1  
                if material in soup[soup_num]['recipeMaterial']:
                    combi[0][material] = 1  

            #ジャンルの入力
            combi[0]['main_genre'] = main[main_num]['genre']
            combi[0]['sub_genre'] = sub[sub_num]['genre']
            combi[0]['soup_genre'] = soup[soup_num]['genre']

            #作成した1列のデータをtrain.csvに追加する
            train_model_writer.writerow(combi[0].values())

        f.flush()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        #ユーザーデータでモデルを作成
        model_make_df = pd.read_csv('train_model.csv', index_col=0)
        user_model = model_make(model_make_df)

    #元データの復元
    shutil.copyfile("train_model_origin.csv", "train_model.csv")


    #ユーザーモデルで予測する
    train = pd.read_csv('train.csv', index_col=0)
    sub_df = pd.read_csv('rakuten_sub.csv', index_col=0)      
    soup_df = pd.read_csv('rakuten_soup.csv', index_col=0)    
    train.reset_index(drop=True, inplace=True)

    #main_genreのonehot
    add_columns = pd.DataFrame(np.zeros(4).reshape(1, 4), columns=['main_genre_1', 'main_genre_2', 'main_genre_3', 'main_genre_4'])
    for add_col in add_columns:
        train[add_col] = 0
    train.drop('main_genre', axis=1, inplace=True)
    main_genre_get = 'main_genre_' + main[main_num]['genre']
    train[main_genre_get] = 1
    
    #sub_genreのonehot
    train = pd.get_dummies(train, columns=['sub_genre'])

    #soup_genreのonehot
    #データの中に汁なしがあるかどうか
    if 0 not in train['soup_genre']:
        train = pd.get_dummies(train, columns=['soup_genre'])
    elif 0 in train['soup_genre']:
        train['soup_genre_0'] = 1 
        train[['soup_genre_1', 'soup_genre_2', 'soup_genre_3', 'soup_genre_4']] = 0
        train.drop('soup_genre', axis=1, inplace=True)

    #主菜、副菜、汁物のジャンル(和、洋、中、その他)ごとのトータル
    train['genre_total_1'] = train['main_genre_1'] + train['sub_genre_1'] + train['soup_genre_1']
    train['genre_total_2'] = train['main_genre_2'] + train['sub_genre_2'] + train['soup_genre_2']
    train['genre_total_3'] = train['main_genre_3'] + train['sub_genre_3'] + train['soup_genre_3']
    train['genre_total_4'] = train['main_genre_4'] + train['sub_genre_4'] + train['soup_genre_4']

    #元データを残しておく
    train_origin = train.copy(deep=True)

    #特徴量の追加
    #train = features.features(train)

    train.drop(['ID', '主菜', '副菜', '汁物', '主菜ID', '採用/不採用'], axis=1, inplace=True)

    #モデルを使って予想
    pred = user_model.predict_proba(train)
    pred_sort_index = np.argsort(pred[:, 0])
    #print(np.abs(np.sort(-pred[:, 1]))[:10])

    #コピーしておいた元データから上位50件の副菜、汁物の名前リストを作成
    sub_name_list = []
    soup_name_list = []
    for i in range(50):
        #予測した副菜のリスト作成
        sub_name = train_origin.iloc[pred_sort_index[i]]['副菜']
        sub_name = sub_df[sub_df['recipeTitle']==sub_name]['recipeId'].values[0]  
        sub_name_list.append(sub_name)
        #副菜重複削除
        sub_name_list = sorted(set(sub_name_list), key=sub_name_list.index)

        #予測した汁物のリスト作成
        soup_name = train_origin.iloc[pred_sort_index[i]]['汁物']
        soup_name = soup_df[soup_df['recipeTitle']==soup_name]['recipeId'].values[0]    
        soup_name_list.append(soup_name)
        #汁物重複削除
        if soup_name_list[0] != 0:     #if soup_name_list[0] !='なし':
            soup_name_list = sorted(set(soup_name_list), key=soup_name_list.index)

    params = {
        'main_num': main_num,
        'sub_name_list': sub_name_list,
        'soup_name_list': soup_name_list,
    }
    return params

###################################################################################################



