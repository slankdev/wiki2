
# Sphinx ドキュメント

```
$ sudo pip3 install sphinx sphinx_rtd_theme

$ sudo apt install -y texlive-fonts-recommended \
		texlive-latex-recommended texlive-latex-extra \
		texlive-lang-japanese latexmk texlive-latex-base

$ brew cask install mactex // make latexpdfでlatexmkを使う
```

## テーマ変更

```
html_theme = 'sphinx_rtd_theme'
```

## Markdownを使う方法

recommonmarkというのを使えばいけるらしい
なおindexページで使うことは想定していない.
参照される記事の一つとして使う.

```
$ sudo pip install commonmark recommonmark
$ cd /path/to/sphinx
$ vim conf.py
...
- source_suffix = ['.rst']
+ source_suffix = ['.rst', '.md']

+ from recommonmark.parser import CommonMarkParser
+ source_parsers = {
+ 	'.md': CommonMarkParser,
+ }
...
$ make html
```

画像を使う時の注意

```
![hogehoge](img.png) // これだといける
![](img.png) // これだといけない
```

生のhtmlの書き込みはうまく処理されないことが多い?

## PDF出力

conf.py
```
language = 'ja'
latex_docclass = {'manual': 'jsbook'}
```

```
$ mkae latexpdf
```




