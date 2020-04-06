
# TeX環境構築

## Install

```
$ sudo apt install texlive
$ sudo apt install texlive-lang-cjk
$ sudo apt install texlive-fonts-recommended texlive-fonts-extra
```

## File Type

| Filetype | description                            |
|:--------:|:--------------------------------------:|
| tex      | ソースファイル                         |
| log      | log                                    |
| aux      | 情報参照用のファイル                   |
| dvi      | DeVice Independent (標準的なTexの出力) |
| cls      | クラスを定義するファイル               |
| clo      | クラスオプションを定義するファイル     |
| sty      | パッケージを定義するファイル           |



## Example

```
\documentclass{jsarticle}
\begin{document}

吾輩は猫である。名前はまだ無い。

どこで生れたかとんと見当がつかぬ。
何でも薄暗いじめじめした所で
ニャーニャー泣いていた事だけは記憶している。
吾輩はここで始めて人間というものを見た。

\end{document}
```


