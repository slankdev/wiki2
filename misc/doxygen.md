
# Doxygen 使い方

## 作業内容

1. 設定ファイルを生成する
2. doxygenを実行する
3. ソースのドキュメント付け

```
$ cd PROJPATH
$ doxygen -g
$ vi program.h
$ vi Doxyfile
$ doxygen
```

```
$ vi Doxyfile
...
- PROJECT_NAME           = "My Project"
+ PROJECT_NAME           = "Project SLANKDEV"

- PROJECT_NUMBER         =
- PROJECT_NUMBER         = "0.0.1"

- EXTRACT_ALL            = NO
+ EXTRACT_ALL            = YES

- RECURSIVE              = NO
+ RECURSIVE              = YES

- GENERATE_LATEX         = YES
+ GENERATE_LATEX         = NO
...
```

```cpp
/**
 * @file lib.h
 * @brief geneus library
 * @author Hiroki SHIROKURA
 * @date 2017.09.24
 * @details
 *   This module include super ultra great
 *   delicious daisyarin yamaarashi
 */

#pragma once

/**
 * @brief
 * @param[in]
 * @param[out]
 * @return void
 * @details
 */
void super_function(int a, int b);


/**
 * @brief
 * @param[in] aa description
 * @param[in] bb description
 * @param[out]
 * @return void
 * @details
 */
void ulutra_function(int aa, int bb);

/**
 * @brief
 * @details
 */
class happy_class {
 private:

  /**
   * detail text..
   */
  int priv_a;

 protected:
  int prot_a; //! detail shot prot_a text...
  int prot_b; //! detail shot prot_b text...

 public:
  int pub_a; //! detail shot text..

  /**
   * @brief
   * @details
   */
  happy_class();

  /**
   * @brief
   * @details
   */
  void func();
};
```


## 設定ファイルパラメータ


| name                    | description                       |
|:-----------------------:|:---------------------------------:|
| PROJECT\_NAME           | Project name                      |
| PROJECT\_NUMBER         | Version                           |
| OUTPUT\_DIRECTORY       | Output Directory Path             |
| INPUT                   | Input Path                        |
| FILE\_PATTERNS          | Specilize Language (*.cc, *.md)   |
| RECURSIVE               | Search files Recursive            |
| SOURCE\_BROWSER         | Generate Source List              |



```
# Sample Doxyfile

INPUT = ../slankdev

PROJECT_NAME            = Lib SLANKDEV
FILE_PATTERN            = *.h
PREDEFINED              = __DOXYGEN__  __attribute__(x)=
OUTPUT_DIRECTORY        = /tmp/libslankdev/
RECURSIVE               = YES
OPTIMIZE_OUTPUT_FOR_C   = YES
ENABLE_PREPROCESSING    = YES
MACRO_EXPANSION         = YES
EXPAND_ONLY_PREDEF      = YES
EXTRACT_STATIC          = YES
EXTRACT_ALL             = YES
DISTRIBUTE_GROUP_DOC    = YES
HIDE_UNDOC_MEMBERS      = YES
HIDE_UNDOC_CLASSES      = YES
HIDE_SCOPE_NAMES        = YES
GENERATE_DEPRECATEDLIST = NO
GENERATE_LATEX          = NO
VERBATIM_HEADERS        = NO
ALPHABETICAL_INDEX      = NO
HTML_TIMESTAMP          = NO
HTML_DYNAMIC_SECTIONS   = YES
SEARCHENGINE            = NO
SORT_MEMBER_DOCS        = NO
SOURCE_BROWSER          = YES
EXAMPLE_PATH            = examples
EXAMPLE_PATTERNS        = *.cc
EXAMPLE_RECURSIVE       = YES
INLINE_SOURCES          = YES
```

