--ドリンクの基本情報のテーブル
CREATE TABLE drink_table(
    drink_id INT AUTO_INCREMENT,
    drink_image VARCHAR(255),
    drink_name VARCHAR(255),
    price INT,
    edit_date DATETIME,
    update_date DATETIME,
    status INT,
    PRIMARY KEY (drink_id)
);

--ドリンクの在庫数情報のテーブル
CREATE TABLE stock_table(
    drink_id INT AUTO_INCREMENT,
    drink_name VARCHAR(255),
    stock INT,
    edit_date DATETIME,
    update_date DATETIME,
    PRIMARY KEY (drink_id)
    );

--ドリンクの購入情報のテーブル
CREATE TABLE history_table(
    drink_id INT(255),
    order_date DATETIME
    );