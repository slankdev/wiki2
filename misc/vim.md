
# Vim

## 複数ファイルに渡って一括文字列置換

 - args 新規リスト作成 ある場合は上書き
 - argadd リストに追加
 - argdelete リストから消去
 - argdo リストにコマンドなどを実行

```
:args a.txt b.txt c.txt
:argdelete c.txt
:argadd f.txt g.txt
:argdo :%s/abc/xyz/g | :update
```

## ユーザ権限で開いたvimで管理者権限で書き込み

```
:w !sudo tee % > /dev/null
```

## Or検索

```
/hoge\|fuga # カッコ必要ダトオモッテイタケドナクテモイケルゼ
```
