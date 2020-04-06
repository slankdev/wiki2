
# Git Command チートシート

```
$ git config --global --edit // 危険
$ git config --local --edit
$ cat .git/config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
[remote "origin"]
        url = https://github.com/slankdev/wiki
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
        remote = origin
        merge = refs/heads/master
[user]
        name = Hiroki Shirokura
				mail = slankdev@nttv6.jp
```

## Gerrit

checkout my working tree
```
$ git ls-remote | grep refs/changes/.*/21357
From ssh://slankdev@gerrit.fd.io:29418/vpp.git
5e634596504e63b1b62a07191d13519290c937bb        refs/changes/57/21357/1
0a7d3dc977aa0717219290bd9d53e025ca45abf0        refs/changes/57/21357/2
2d64f780cc9a65800882fafa95838e5f02f25014        refs/changes/57/21357/3
47848805d40165d1d06149595d7951e2ceea26e8        refs/changes/57/21357/4
c68aeb981e5b616014d5c0f0a9bdbedea281918c        refs/changes/57/21357/5

[1]
$ git review -d 12357

[2]
$ git pull origin refs/changes/57/21357/5
$ git rebase

[3] best-way
$ git fetch origin refs/changes/57/21357/5
$ git checkout -b work FETCH_HEAD

$ vim ...
$ git add .
$ git commit -s --amend
```

## リモートリポジトリ関係

リモートにタグをうつ
```
$ git clone <repo> && cd <repo>
$ git tag <tagname>
$ git push origin <tagname>
```

リモートのタグ消去
```
$ git clone <repo> && cd <repo>
$ git tag -d TAG
$ git push origin :TAG
```

origin/branch-nameを消去する

```
$ git branch -d BRANCHNAME
$ git push origin :BRANCHNAME
```

リモートブランチからローカルブランチを切る

```
$ git checkout -b branch-name origin/branch-name

// 以下でも同じ
$ git checkout origin/branch-name
$ git checkout -b branch-name
```

リモートブランチにpushする

```
$ git push origin local-name:remote-name
```

リモートブランチ同士でマージする

AブランチをBブランチにマージする

作業の流れはこんな感じ

```
       *  *
       |  |
 B(old)*  *A
       | /
	   |/
 B(new)*
```


```
$ git branch
* master
  A
  B
$ git checkout B
$ git mearge --no-ff A
```

これでおっけい



.gitignoreされていないファイルを一括消去

```
$ git rm --cached `git ls-files --full-name -i --exclude-from=.gitignore`
```


addの取り消し

これでaddだけを取り消せる. ファイルの変更などは保持される

```
$ git reset HEAD sample.txt
```

タグの打ち方 push方法

追加
```
$ git tag TAGNAME
$ git push --tags
```

消去
```
$ git tag -d TAGNAME
$ git push origin :TAGNAME
```

タグのcheckoutほうほう

```
$ git checkout -b <name> refs/tags/<tagname>
```

## Forking Tech

```
$ git clone https://github.com/slankdev/linux.git linux && cd $_
$ git remote add upstream https://github.com/torvalds/linux.git
$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/upstream/master

$ git fetch upstream
remote: Counting objects: 1, done.
remote: Total 1 (delta 0), reused 1 (delta 0)
Unpacking objects: 100% (1/1), done.
From git://github.com/DQNEO/Renshu
 * [new branch]      develop    -> upstream/develop
 * [new branch]      master     -> upstream/master

$ git merge upstream/master
```

## Fix Author

```
git log -1 --pretty=full
commit befdbcd2389373088fe3e83d9c0d401a9de7717d
Author: hogehoge <dummy@example.com>
Commit: fugafuga <test@example.com>

    add test.txt

git config --local user.name Hiroki Shirokura
git config --local user.email slank.dev@gmail.com
git commit --amend --author="Hiroki Shirokura <slank.dev@gmail.com>"

git log --pretty=full
commit befdbcd2389373088fe3e83d9c0d401a9de7717d
Author: Hiroki Shirokura <slank.dev@gmail.com>
Commit: Hiroki Shirokura <slank.dev@gmail.com>

    add test.txt
```

## Config

```
git config --global color.ui true
```
