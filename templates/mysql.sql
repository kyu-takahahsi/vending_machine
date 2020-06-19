--11章
create database mydb;
--課題1
--character_table作成、データ挿入、表示
CREATE TABLE character_table(
    character_id INT(100),
    character_name VARCHAR(100),
    pref VARCHAR(10)
    );

INSERT INTO character_table(character_id, character_name, pref) VALUES (1, 'ふなっしー', '千葉県');
INSERT INTO character_table(character_id, character_name, pref) VALUES (2, 'ひこにゃん', '滋賀県');
INSERT INTO character_table(character_id, character_name, pref) VALUES (3, 'まりもっこり', '北海道');

SELECT *
FROM character_table;


--emp_table作成、データ挿入、表示
CREATE TABLE emp_table(
    emp_id INT(100),
    emp_name VARCHAR(100),
    job VARCHAR(100),
    age INT(100)
    );

INSERT INTO emp_table(emp_id, emp_name, job, age) VALUES (1, '山田太郎', 'manager', 50);
INSERT INTO emp_table(emp_id, emp_name, job, age) VALUES (2, '伊藤静香', 'manager', 45);
INSERT INTO emp_table(emp_id, emp_name, job, age) VALUES (3, '鈴木三郎', 'analyst', 30);
INSERT INTO emp_table(emp_id, emp_name, job, age) VALUES (4, '山田花子', 'clerk', 24);

SELECT *
FROM emp_table;


--課題2
--goods_table表示
SELECT *
FROM goods_table
WHERE price<=500;

--character_table表示
SELECT DISTINCT
       character_id,
       character_name
FROM character_table
WHERE pref LIKE "%県";

--emp_table表示
SELECT emp_id,
       age
FROM emp_table
WHERE job="clerk";

--emp_table表示
SELECT emp_id,
       emp_name
FROM emp_table
WHERE job="analyst" or age BETWEEN 20 AND 25;



--課題3
--emp_tableのemp_id1のjobをCTOに更新
UPDATE emp_table SET job = "CTO" WHERE emp_id = 1;

SELECT *
FROM emp_table;

--emp_tableのage>=40のレコードを削除
DELETE FROM emp_table WHERE age>=40;

SELECT *
FROM emp_table;

--13章
CREATE TABLE Bulletin_board(
    add_id INT(255),
    add_name VARCHAR(1000),
    add_comment VARCHAR(1000),
    add_time VARCHAR(1000)
    );
SELECT *
FROM Bulletin_board;

DELETE FROM Bulletin_board WHERE add_time = "GETDATE()";

--15章
CREATE TABLE order_table(
    order_id INT(255),
    customer_id INT(255),
    order_date VARCHAR(100),
    payment VARCHAR(100)
    );


DELETE FROM order_table;
INSERT INTO order_table (order_id, customer_id, order_date, payment) VALUES
(1, 1, '2017-10-01 10:22:30', 'クレジット'),(2, 2, '2017-10-01 18:51:06', 'クレジット'),(3, 3, '2017-10-02 09:14:35', '代金引換'),(4, 1, '2017-10-03 11:00:57', 'クレジット');


CREATE TABLE order_detail_table(
    order_id INT(255),
    goods_id INT(255),
    quantity INT(100)
    );

DELETE FROM order_detail_table;
INSERT INTO order_detail_table (order_id, goods_id, quantity) VALUES
(1, 1, 3),(1, 5, 3),(2, 2, 1),(3, 1, 10),(3, 4, 10),(4, 1, 5);



CREATE TABLE customer_table(
    customer_id INT(255),
    customer_name VARCHAR(100),
    address VARCHAR(100),
    phone_number VARCHAR(50)
    );

DELETE FROM customer_table;
INSERT INTO customer_table (customer_id, customer_name, address, phone_number) VALUES
(1, '佐藤一郎', '東京都港区六本木6-10-1', '0345670000'),(2, '鈴木誠', '神奈川県横浜市中区立野2-1', '09099991111'),(3, '山田葵', '東京都杉並区今川5-3', '0378902222');


--15章課題1
--例1
SELECT
    order_customer.order_id as order_id,
    order_customer.order_date as order_date,
    order_customer.payment as payment,
    order_customer.customer_name as customer_name,
    order_customer.address as address,
    order_customer.phone_number as phone_number,
    goods_order.goods_name as goods_name,
    goods_order.price as price,
    goods_order.quantity as quantity
FROM
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
JOIN
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
ON
    order_customer.order_id = goods_order.order_id;

--例2
SELECT
    order_customer.order_id as order_id,
    order_customer.order_date as order_date,
    order_customer.customer_name as customer_name,
    goods_order.goods_name as goods_name,
    goods_order.price as price,
    goods_order.quantity as quantity
FROM
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
JOIN
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
ON
    order_customer.order_id = goods_order.order_id
WHERE
    customer_name = '佐藤一郎';

--例3
SELECT
    goods_order.goods_name as goods_name,
    goods_order.price as price,
    goods_order.quantity as quantity,
    order_customer.order_date as order_date
FROM
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    LEFT JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
JOIN
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
ON
    goods_order.order_id = order_customer.order_id
WHERE
    goods_name = 'コーラ';

--例4
SELECT
    goods_order.goods_name as goods_name,
    goods_order.price as price,
    goods_order.quantity as quantity,
    order_customer.order_date as order_date
FROM
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    LEFT JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
LEFT JOIN
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
ON
    goods_order.order_id = order_customer.order_id
ORDER BY quantity DESC;

--16章課題
--例1
SELECT
    order_customer.customer_name as customer_name,
    COUNT(order_customer.customer_name) as order_count
FROM
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
JOIN
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
ON
    goods_order.order_id = order_customer.order_id

GROUP BY customer_name
ORDER BY order_count DESC;

--例2
SELECT
    goods_order.goods_name as goods_name,
    COUNT(goods_order.goods_name) as goods_order_count
FROM
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    LEFT JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
LEFT JOIN
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
ON
    goods_order.order_id = order_customer.order_id
WHERE
    price = 100

GROUP BY goods_name
ORDER BY goods_order_count DESC;

--例3
SELECT
    order_customer.customer_name as customer_name,
    SUM(goods_order.price) as total_price
FROM
    (
    SELECT
        gt.goods_name as goods_name,
        gt.price as price,
        odt.quantity as quantity,
        odt.order_id as order_id
    FROM
        goods_table as gt
    JOIN
        order_detail_table as odt
    ON
        gt.goods_id = odt.goods_id
    ) as goods_order
JOIN
    (
    SELECT
        ot.order_id as order_id,
        ot.order_date as order_date,
        ot.payment as payment,
        ct.customer_name as customer_name,
        ct.address as address,
        ct.phone_number as phone_number
    FROM
        order_table as ot
    JOIN
        customer_table as ct
    ON
        ot.customer_id = ct.customer_id
    ) as order_customer
ON
    goods_order.order_id = order_customer.order_id
GROUP BY customer_name
ORDER BY total_price DESC;

--18章
CREATE TABLE drink_table(
    --drink_id INT AUTO_INCREMENT,
    drink_image LONGBLOB,
    drink_name VARCHAR(255),
    price INT,
    edit_date DATETIME,
    update_date DATETIME,
    status INT,
    PRIMARY KEY (drink_id)
);


CREATE TABLE stock_table(
    --drink_id INT AUTO_INCREMENT,
    drink_name VARCHAR(255),
    stock INT,
    edit_date DATETIME,
    update_date DATETIME,
    PRIMARY KEY (drink_id)
    );

CREATE TABLE history_table(
    drink_id INT(255),
    order_date DATETIME
    );

--結合
SELECT dt.drink_image as drink_image, dt.drink_id as drink_id, dt.drink_name as drink_name, dt.price as price, st.stock as stock, dt.status as status FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id

--INSERT INTO drink_table (add_image, add_name, add_price, add_number, edit_date, update_date, status) VALUES ('{add_image}', '{add_name}', {add_price}, {add_number}, LOCALTIME(), LOCALTIME(), {status_selector})
--INSERT INTO stock_table (stock, edit_date, update_date) VALUES (stock, LOCALTIME(), LOCALTIME())
--INSERT INTO history_table (order_date) VALUES (LOCALTIME())

SELECT dt.drink_image as drink_image, dt.drink_name as drink_name, dt.price as price, st.stock as stock FROM drink_table as dt LEFT JOIN stock_table as st ON dt.drink_id = st.drink_id

