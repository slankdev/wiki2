
Netlink Book :: はじめに
=========================

netlinkはLinux kernelのNetwork機能をはじめ, さまざなな機能のconfigurationに使われるMessage BUSインターフェースです.
ここではNetlinkの基本的な仕組みと, その利用方法に関してサンプルコードをベースに説明します. 基本的なC言語のプログラミング
の基礎知識を持つ読者が本reportを読むことによって, Netlinkを用いてLinuxのnetwork機能を直接configurationできるレベルに成長できます.
おそらく本書の読者はiproute2はもちろん叩いたことがあると思いますが, 本書ではiproute2と同じ能力をもったプログラムを自作することが
できるようになることが目標です.

NetlinkはLinuxのNetwork機能を理解する上で非常に重要なInterfaceであり,なぜこのようなことが必要なのかどうかは本書を
読み進めていただければ理解できると思います.

本書では以下のような議題でNetlinkを整理します.

.. code-block:: text

  - Netlinkとはなにか
    - Netlinkはどこで使われているか
      - iproute2
      - Routing Software (FRR)
      - Network OS
    - Netlinkを理解する意義はなにか
  - Netlinkの基本,Msgの種類のざっくりとした紹介
    - サンプルコード
    - デバッグ方法
  - 実際のnetlink Messageを解析しながら構造を理解する.
    - iproute2の送信するNetlink msgをトレースしてみる.
    - 簡単な経路を追加するアプリケーション.

