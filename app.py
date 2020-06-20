from flask import Flask
app = Flask(__name__)
#HTMLに反映
from flask import render_template
#HTMLから抽出
from flask import request
#ランダム選択
import random
#データベース操作
import mysql.connector
from mysql.connector import errorcode
#正規表現
import re
#時間取得
import datetime
#18章ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
#管理者画面
@app.route("/admin", methods=["GET", "POST"])
def admin():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'kaA1ybB2ucC3d2c'    # MySQLのパスワード
    dbname   = 'mydb'    # データベース名


    #変数定義ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #追加
    add_image = ""
    add_name = ""
    add_price = ""
    add_number = ""
    status_selector = ""

    #HTML受け渡し(判定)
    goods = ""
    add_message = ""
    change_message = ""

    #ステータス変更
    change_status = ""
    update_status = ""

    #在庫数変更
    change_stock = ""
    change_stock_id = ""
    update_stock = ""


    #ボタンが押された場合にしか値を受け取らないーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #商品追加された場合、値を取得
    if "add_drink" in request.form.keys():
        add_image = request.files.get("file")
        add_name = request.form.get("add_name")
        add_price = request.form.get("add_price")
        add_number = request.form.get("add_number")
        status_selector = request.form.get("status_selector","")

    #ステータス変更された場合、値を取得
    if "change_status" in request.form.keys():
        change_status = int(request.form.get("change_status"))

    #在庫数が変更された場合、値を取得
    if "change_stock_id" in request.form.keys():
        change_stock = request.form.get("change_stock")
        change_stock_id = int(request.form.get("change_stock_id"))
        #在庫数の値が数字ならint型に、文字列なら"文字列"に、空欄なら""に
        if change_stock != None and change_stock != "" and change_stock.isdecimal() == True:
            change_stock = int(request.form.get("change_stock"))
        elif change_stock != None and change_stock != "" and change_stock.isdecimal() == False:
            change_stock = "文字列"
        else:
            change_stock = ""


    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try :
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #常時実行するSQL
        query = "SELECT  dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id"

        #SQL実行
        cursor.execute(query)


        #SQLで取得した値を格納(HTMLに送るためのリスト)
        goods = []
        for (id, image, name, price, stock, status) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "stock" : stock, "status" : status}
            goods.append(item)
            #ステータス変更ボタンの押された商品のidと同じ商品の情報を変数に格納
            if item["id"] == change_status:
                update_status = item
            #在庫数変更ボタンの押された商品のidと同じ商品の情報を変数に格納
            if item["id"] == change_stock_id:
                update_stock = item


        #商品追加のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        if "add_drink" in request.form.keys():
            #全ての項目が入力され、値段と在庫数が整数の場合
            if (add_image != "" and add_name != "" and add_price != "" and add_number != "" and status_selector != "") and (add_number.isdecimal() == True and add_price.isdecimal() == True) and (int(add_price) >= 0 and int(add_number) >= 0) :
                drink_query = f"INSERT INTO drink_table (drink_image, drink_name, price, edit_date, update_date, status) VALUES ('{add_image}', '{add_name}', {add_price}, LOCALTIME(), LOCALTIME(), {status_selector})"
                stock_query = f"INSERT INTO stock_table (drink_name, stock, edit_date, update_date) VALUES ('{add_name}', {add_number}, LOCALTIME(), LOCALTIME())"
                cursor.execute(drink_query)
                cursor.execute(stock_query)
                cnx.commit()
                add_message = "＊追加成功：商品が正常に追加されました"

            #条件にあっていない入力や空欄がある
            else:
                add_message = "＊追加失敗：全ての項目を条件通り入力してください"


        #在庫変更のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        elif "change_stock_id" in request.form.keys():
            #入力欄の値が変更されたときのみデータベース更新
            if update_stock["stock"] != change_stock and change_stock != "" and (change_stock != "文字列" and change_stock != "") :
                stock_update_query_1 = f'UPDATE stock_table SET stock = {change_stock}, update_date = LOCALTIME() WHERE drink_id = {update_stock["id"]}'
                stock_update_query_2 = f'UPDATE drink_table SET update_date = LOCALTIME() WHERE drink_id = {update_stock["id"]}'
                cursor.execute(stock_update_query_1)
                cursor.execute(stock_update_query_2)
                cnx.commit()
                change_message = "＊成功：" + update_stock["name"] + "の在庫数が変更されました"

            #入力欄の値が文字列で入力されている
            elif update_stock["stock"] != change_stock and change_stock == "文字列":
                change_message = "＊エラー：在庫数の値は0以上の整数で入力してください"

            #入力欄の値が入力されていない
            elif update_stock["stock"] != change_stock and change_stock == "":
                change_message = "＊エラー：在庫数の値を入力してください"

            #入力欄の値が変更されていない
            else:
                change_message = "＊エラー：" + update_stock["name"] + "の値が変更されていません"


        #公開・非公開のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        elif "change_status" in request.form.keys():
            #現在のステータスが公開(1)の場合、非公開(0)に変更
            if update_status["status"] == 1:
                status_update_query_1 = f'UPDATE drink_table SET status = 0 WHERE drink_id = {update_status["id"]}'
                status_update_query_2 = f'UPDATE drink_table SET update_date = LOCALTIME() WHERE drink_id = {update_status["id"]}'
                cursor.execute(status_update_query_1)
                cursor.execute(status_update_query_2)
                cnx.commit()
                change_message = "＊成功：" + update_status["name"] + "を非公開にしました"

            #現在のステータスが非公開(0)の場合、公開(1)に変更
            elif update_status["status"] == 0:
                status_update_query_1 = f'UPDATE drink_table SET status = 1 WHERE drink_id = {update_status["id"]}'
                status_update_query_2 = f'UPDATE drink_table SET update_date = LOCALTIME() WHERE drink_id = {update_status["id"]}'
                cursor.execute(status_update_query_1)
                cursor.execute(status_update_query_2)
                cnx.commit()
                change_message = "＊成功：" + update_status["name"] + "を公開にしました"


        #どのボタンも押されていない場合(最初のページを表示するがここでは何もしない)ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        else:
            pass


        #いつでも実行する表示のためのSQLーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        cursor.execute(query)


        #データベース変更後に再度リストに格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        goods = []
        for (id, image, name, price, stock, status) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "stock" : stock, "status" : status}
            goods.append(item)


        #値の入った変数やリストをHTMLに渡すための変数に格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        params = {
        "add_message" : add_message,
        "change_message" : change_message,
        "goods" : goods
        }


    #もしユーザー名やパスワードなどに誤りがあった場合エラーを出すーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()


    #HTMLへ変数を送るーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    return render_template("admin.html", **params)


#購入者画面-----------------------------------------------------------------
@app.route("/user", methods=["GET", "POST"])
def user():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'kaA1ybB2ucC3d2c'    # MySQLのパスワード
    dbname   = 'mydb'    # データベース名


    #変数定義ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #購入
    my_money = ""
    select_button = ""

    #HTML受け渡し(判定)
    message = ""
    judge_money = ""
    judge_select = ""
    home = ""
    success = ""

    #購入金額比較
    bought = ""


    #ボタンが押された場合にしか値を受け取らないーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #商品追加された場合、値を取得
    if "buy_drink" in request.form.keys():
        my_money = request.form.get("my_money")
        select_button = request.form.get("select_button")
        #取得した値がもし文字列や数字ならdrink_idをint型にネスト(下記で条件分岐するため)
        if select_button != None and select_button != "":
            select_button = int(select_button)


    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try :
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #いつでも実行する表示のためのSQLーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        query = "SELECT dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, dt.status as status, st.stock as stock FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id WHERE stock IS NOT NULL and status = 1"
        cursor.execute(query)


       #SQLで取得した値を格納(HTMLに送るためのリスト)ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        goods = []
        for (id, image, name, price, status, stock) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "status" : status, "stock" : stock}
            goods.append(item)
            #商品購入ボタンの押された商品のidと同じ商品の情報を変数に格納
            if item["id"] == select_button:
                bought = item


        #商品購入ボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        if "buy_drink" in request.form.keys():
            #金額・商品共に数字が入力されており、足りている
            if (my_money != "" and my_money.isdecimal() == True) and select_button != None and bought != "":
                my_money = int(my_money)
                bought["price"] = int(bought["price"])
                bought["stock"] = int(bought["stock"])
                if my_money >= bought["price"] and bought["stock"] > 0 and bought["status"] != "0":
                    message = "自動販売機結果"
                    judge_money = "＊ガシャコン！！" + bought["name"] + "が買えました！＊"
                    judge_select = "<<<お釣りは" + str(my_money - bought["price"]) + "円です>>>"
                    #在庫数変更のクエリ
                    stock_update_query = f'UPDATE stock_table SET stock = {bought["stock"]-1} WHERE drink_id = "{bought["id"]}"'
                    history_query = f'INSERT INTO history_table (drink_id,order_date) VALUES ({bought["id"]}, LOCALTIME())'
                    cursor.execute(stock_update_query)
                    cursor.execute(history_query)
                    cnx.commit()
                    success = bought["image"]

                #金額・商品共に入力されているが、在庫がない
                elif my_money >= bought["price"] and bought["stock"] == 0 and bought["status"] != "0":
                    message = "自動販売機結果"
                    judge_money = "＊現在在庫がありません"

                #金額・商品共に入力されているが、金額が足りていない
                else:
                    message = "自動販売機結果"
                    judge_money = "＊お金が" + str(bought["price"] - my_money) + "円足りません"

            #金額・商品共に数字が入力されており、足りているが公開されていない
            elif (my_money != "" and my_money.isdecimal() == True) and select_button != None and bought == "":
                    message = "自動販売機結果"
                    judge_money = "＊申し訳ありません、この商品は現在お売りすることができません"


            #金額入力もしくは商品の選択が行われていない
            elif (my_money == "" or my_money.isdecimal() == False) or select_button == None:
                #金額、商品共に入力されていない
                if my_money == "" and select_button == None:
                    message = "自動販売機結果"
                    judge_money = "＊お金を投入してください"
                    judge_select = "＊商品を選択してください"

                #商品が選択されていない
                elif my_money == "":
                    message = "自動販売機結果"
                    judge_select = "＊お金を投入してください"

                #金額が入力されていない
                elif select_button == None :
                    message = "自動販売機結果"
                    judge_money = "＊商品を選択してください"

                #金額が数字ではない
                else:
                    message = "自動販売機結果"
                    judge_money = "＊金額は数字で入力してください"


        ##どのボタンも押されていない場合(最初のページを表示する)ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        else:
            message = "自動販売機"
            home = "home"


        #値の入った変数やリストをHTMLに渡すための変数に格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        params = {
        "success" : success,
        "judge_money" : judge_money,
        "judge_select" : judge_select,
        "message" : message,
        "goods" : goods,
        "home" : home
        }


    #もしユーザー名やパスワードなどに誤りがあった場合エラーを出すーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    #HTMLへ変数を送るーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    return render_template("user.html", **params)