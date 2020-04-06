
# ReST形式チートシート

コードブロック
```
文章文章

::
	code code
	code code

文章文章
```
```
.. code-block:: python

	import sys
	print sys.path
```

リスト
```
- test
- test

1. test
2. test
3. test
```

外部リンク
```
詳しくは、 http://sphinx-users.jp を参照してください。
`Sphinxを知りたい方はこちらをクリック <http://sphinx-users.jp>`_
Sphinxの詳しい情報源: SphinxJP_
.. _SphinxJP: http://sphinx-users.jp
```

内部リンク
```
.. _sample:

参照は :ref:`sample` としても参照できますし、
:ref:`ほげほげ<sample>` として任意のテキストでも参照できます。
ただし一行開ける必要がある.
```

画像
```
.. image:: ../img/sphinx.png
   :scale: 40%
   :height: 100px
   :width: 200px
   :align: left
```

ノートとTODO
```
.. todo::
  具体的なユースケースを用いてD2が有効であることを示す.
  コアネットワークにデプロイしている状態で思いトラフィックを処理できる場面と
  NFVサービスチェイン環境で軽量なVNFを多数デプロイし, 基盤リソースを効率よく
  共有する場面を例としながら説明する.

.. note::
   This function is not suitable for sending spam e-mails.
```

