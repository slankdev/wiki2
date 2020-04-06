
# Pandoc

```
% タイトル
% 作成者
% 日付

# h1タグで一枚

文章は平打ちします。タイトルページは自動で生成されるので、
このスライドは2枚目です。


# リストもつくれます

記号のリスト

* 書き方は同じです
* いろいろできるんです

数字のリスト

1. 数字も使えます
1. 自動で連番になります。

# ボックス表示

\begin{exampleblock}{exampleblock}
これはTexで記述
\end{exampleblock}
\begin{alertblock}{alertblock}
テーマによって表示されません
\end{alertblock}
\begin{block}{block}
リスト表示
\begin{itemize}
\item リストもかけます
\end{itemize}
\end{block}
```


```
% h-lualatexja.tex
\usepackage{luatexja}
\hypersetup{unicode=true}
```

```
#!/bin/sh

pandoc memo.md \
	-o output.pdf \
	--latex-engine=lualatex \
	-t beamer \
	-V theme:Madrid \
	-V colortheme:seahorse \
	-V fontsize:20pt \
	-H h-lualatexja.tex
```
