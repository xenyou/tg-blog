tg-blog
=======

A turbogears application for blog

## Setup
```
easy_install turbogears==1.1.3
easy_install sqlobject
easy_install kid
easy_install docutils
```

## Install and Run
```
git clone https://github.com/xenyou/tg-blog.git
cd tg-blog
./start-miniascaper2.py
visit http://localhost:8080
```

## How to use it
1. Click [registration] link.
2. Register 1st user (root user) 
3. Login
4. Click [write] link and write an article.

## Note
Setup LANG and LC_ALL environment variables if you use Mac OS X. Otherwise you'll get an error like 'ValueError: unknown locale: UTF-8'.
```
export LANG=ja_JP.UTF-8
export LC_ALL=ja_JP.UTF-8
```

