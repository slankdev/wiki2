
# Travis-CI使い方

C++11を使う場合のテンプレート

```
sudo: false
language: cpp
branches:
  except:
  - develop # developだけ除外する
compiler:
  - clang++
  - g++

install:
  - if [ "$CXX" = "g++" ]; then export CXXFLAGS="-std=c++11"; fi
  - if [ "$CXX" = "g++" ]; then export CXX="g++-5" CC="gcc-5"; fi

addons:
  apt:
    sources:
      - ubuntu-toolchain-r-test
      - llvm-toolchain-precise-3.7
      - llvm-toolchain-precise
    packages:
      - clang-3.7
      - g++-5
      - gcc-5

script:
  - make CXX="${CXX}"
  - ./test
```

```
$ cd repos
$ sudo apt install ruby ruby-dev
$ sudo gem install travis
$ travis login
$ travis sync

// slack integration appからdomain:tokenをコピペ
$ travis encrypt -r owner/repos "domain:token" --add notifications.slack
```





