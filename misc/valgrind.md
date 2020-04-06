

# valgring つかってみた

## なにこれ

 - メモリリーク、二重解放、不正メモリアクセスの検出
 - マルチスレッドに関連した問題の検出
 - 実効時間や呼び出し回数の集計などボトルネックをしらべたり

## 使用方法

```
$ gcc -g main.c
$ cat main.c
#include <stdio.h>
#include <stdlib.h>
int main()
{
    char* p = (char*)malloc(sizeof(char)*5);
    p[6] = 'a';
    free(p);
}
$ valgring ./a.out
```



## メモ

 - デバッグオプションとかをつけた方がいいかも

## Helgrind

```
$ cat main.cc
#include <thread>
#include <pthread.h>

int var = 0;

void child_fn () { var++; }

int main ( void ) {
  std::thread t(child_fn);
  var++;
  t.join();
  return 0;
}
$ g++ -std=c++11 -g -O0 main.cc -lpthread
$ valgrind --tool=helgrind ./a.out
```

