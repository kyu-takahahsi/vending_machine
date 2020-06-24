from flask import Flask, flash, redirect, url_for
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
#画像保存のため
import os
#画像保存のため
from werkzeug.utils import secure_filename
#18章ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'kaA1ybB2ucC3d2c'    # MySQLのパスワード
dbname   = 'mydb'    # データベース名

#管理者画面
#ホーム画面
@app.route("/admin", methods=["GET", "POST"])
def admin():
    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try :
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #常時実行するSQL
        query = "SELECT  dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id"
        cursor.execute(query)


        #SQLで取得した値を格納(HTMLに送るためのリスト)
        goods = []
        for (id, image, name, price, stock, status) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "stock" : stock, "status" : status}
            goods.append(item)


        #値の入った変数やリストをHTMLに渡すための変数に格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        params = {
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


#商品追加画面
@app.route("/admin/add", methods=["POST"])
def admin_add_item():

    #変数定義ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #追加
    add_image = ""
    add_name = ""
    add_price = ""
    add_number = ""
    status_selector = ""
    filename = ""

    #HTML受け渡し(判定)
    add_message = ""

    #ボタンが押された場合にしか値を受け取らないーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    #商品追加された場合、値を取得
    if "add_drink" in request.form.keys():
        add_image = request.files.get("add_image")
        add_name = request.form.get("add_name")
        add_price = request.form.get("add_price")
        add_number = request.form.get("add_number")
        status_selector = request.form.get("status_selector")
        #これでformから受け取った画像を保存する
        filename = secure_filename(add_image.filename)
        if filename != "" and filename != None:
            add_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            add_image = ""


    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try :
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #常時実行するSQL
        query = "SELECT  dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id"

        #SQLに画像のパスを保存する
        if add_image != "" and add_image != None:
            drink_image = "../static/" + filename


        #商品追加のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        if "add_drink" in request.form.keys():
            #全ての項目が入力されていない
            if add_image == "" or add_name == "" or add_price == "" or add_number == "" or status_selector == "":
                add_message = "＊追加失敗：全ての項目を条件通り入力してください"

            #在庫数と値段の値が数字ではない
            elif not add_number.isdecimal() or not add_price.isdecimal():
                add_message = "＊追加失敗：在庫数と値段は数字で入力してください"

            elif int(add_price) < 0 or int(add_number) < 0:
                add_message = "＊追加失敗：在庫数と値段は0以上の数字で入力してください"

            #全て入力され、在庫数と値段は0以上の数字(条件通り)
            else:
                drink_query = f"INSERT INTO drink_table (drink_image, drink_name, price, edit_date, update_date, status) VALUES ('{drink_image}', '{add_name}', {add_price}, LOCALTIME(), LOCALTIME(), {status_selector})"
                stock_query = f"INSERT INTO stock_table (drink_name, stock, edit_date, update_date) VALUES ('{add_name}', {add_number}, LOCALTIME(), LOCALTIME())"
                cursor.execute(drink_query)
                cursor.execute(stock_query)
                cnx.commit()
                add_message = "＊追加成功：商品が正常に追加されました"


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


#在庫数変更
@app.route("/admin/stock", methods=["POST"])
def admin_stock():

    #在庫数変更の商品情報
    drink_id = ""
    drink_name = ""
    stock = ""

    #メッセージ
    change_message = ""


    #在庫数が変更された場合、値を取得
    if "change_stock" in request.form.keys():
        drink_id = request.form.get("drink_id")
        drink_name = request.form.get("drink_name")
        stock = request.form.get("stock")


    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #在庫変更のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        if "change_stock" in request.form.keys():#うまい具合にNoneにならなければ消そうね
            #空欄
            if stock == "":
                change_message = "＊失敗：金額は空欄ではなく0以上の数字を入力してください"

            #文字列もしくはマイナスの値
            elif not stock.isdecimal() or int(stock) < 0:
                change_message = "＊失敗：金額は0以上の数字で入力してください"

            #0以上の数字(条件通り)
            else:
                stock_update = f'UPDATE stock_table SET stock = {stock} WHERE drink_id = {drink_id}'
                date_update = f'UPDATE stock_table SET update_date = LOCALTIME() WHERE drink_id = {drink_id}'
                cursor.execute(stock_update)
                cursor.execute(date_update)
                cnx.commit()
                change_message = "＊成功：" + drink_name + "の在庫数が変更されました"


        #常時実行するSQL
        query = "SELECT  dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id"
        cursor.execute(query)


        #SQLで取得した値を格納(HTMLに送るためのリスト)
        goods = []
        for (id, image, name, price, stock, status) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "stock" : stock, "status" : status}
            goods.append(item)


        #値の入った変数やリストをHTMLに渡すための変数に格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        params = {
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


#ステータス変更
@app.route("/admin/status", methods=["POST"])
def admin_status():

    #ステータス変更の商品情報
    drink_id = ""
    drink_name = ""
    next_status = ""

    #メッセージ
    change_message = ""


    #ステータス変更が押された場合、値を取得
    if "change_status" in request.form.keys():
        drink_id = request.form.get("drink_id")
        drink_name = request.form.get("drink_name")
        next_status = request.form.get("change_status")


    #mysqlに接続ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    try :
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        #公開・非公開のボタンが押された場合ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        if "change_status" in request.form.keys():
            #押されたボタン(現在のステータス)とは逆のステータスに変更
            if drink_id != "" and drink_id != None:
                status_update = f'UPDATE drink_table SET status = {next_status} WHERE drink_id = {drink_id}'
                date_update = f'UPDATE drink_table SET update_date = LOCALTIME() WHERE drink_id = {drink_id}'
                cursor.execute(status_update)
                cursor.execute(date_update)
                cnx.commit()
                if next_status == "1":
                    change_message = "＊成功：" + drink_name + "のステータスを「公開」に変更しました"
                elif next_status == "0":
                    change_message = "＊成功：" + drink_name + "のステータスを「非公開」に変更しました"


        #常時実行するSQL
        query = "SELECT  dt.drink_id as drink_id, dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id"
        cursor.execute(query)


        #SQLで取得した値を格納(HTMLに送るためのリスト)
        goods = []
        for (id, image, name, price, stock, status) in cursor:
            item = {"id" : id, "image" : image, "name" : name, "price" : price, "stock" : stock, "status" : status}
            goods.append(item)


        #値の入った変数やリストをHTMLに渡すための変数に格納ーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        params = {
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
                    history_query = f'INSERT INTO history_table (drink_id, order_date) VALUES ({bought["id"]}, LOCALTIME())'
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
