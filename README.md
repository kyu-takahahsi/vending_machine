【18章】自動販売機課題  
ーーーーーーーーーーーーーーーーーーーーーーーーーー  
「伝えたいこと」  
・自分なりに前回までの修正を見直して改良しましたが、まだまだ足りない部分があると思うので  
　お手柔らかにお願いします。  
ーーーーーーーーーーーーーーーーーーーーーーーーーー  
「処理とURL」  
＊管理者画面  
・/admin：商品の一覧が表示される処理  
・/admin/add：商品を追加するための処理  
・/admin/stock：商品の在庫変更のための処理  
・/admin/status：商品のステータス変更のための処理  
  
＊購入者画面  
・/admin：商品を購入するための処理  
ーーーーーーーーーーーーーーーーーーーーーーーーーー  
「前回から変更した点の説明」  
・元々管理者、購入者の2つの処理/URLしかなかったが、5つに分割(処理ごと)  
・if文の改良(異常値を先に書き、同じような条件を極力書かないように)  
・ステータス変更の処理で現在のデータベースと比較して反対にするという流れにしていたが、  
　押されたボタンに入っている値通りにステータスを変更するように(同時に管理者が開いていた場合でも問題が起きない)  
　また押されたボタンのvalueに変更後のステータスの値を入れて、どちらが押されても条件分岐せず同じ処理を行うように  
　(一見同じクエリだが変数の中身によって変えている)  
・ Python側で現在の値を取得するのではなく、HTML側でtype=hiddenを使うことで必要な情報を取得  
ーーーーーーーーーーーーーーーーーーーーーーーーーー

