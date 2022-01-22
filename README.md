### 1.为什么选择开源

本项目是一个外包项目，但是项目做完了，项目方不要了。

这个项目有当时做的时候闹了几个乌龙事件，当时客户要的是零 JS 代码，但是我们确做偏了。第一次提交给客户的代码含有好多好多 JS 😂。

项目合同期是 2 个星期，但是项目确历时了 1 个多月。为什么这样呢，其实这个项目代码还有一版后端 golang 写的，前端是 Vue，Golang 写的那版不符合客户要求，里面包含好多好多 JS 😂，后来才改成用 Django 来写，所以时间故而就拉长了。

Golang 开发的那版，我们也会开源，因为整个项目都没有交付给客户，不会产生合同纠纷，因此想把这个代码开放出来供大家学习和使用。

### 2.项目介绍

本项目分为前端 PC 和 操作管理台，因为是零 JS 代码，操作体验比较差一些，但是整体的逻辑和项目是顺畅。

本项目是一个区块链商城平台，区块链相关部分没有包含在这个代码里面，当然，也不会开源哈。

### 3.项目部署

在部署代码前，你需要安装 python 3.8 以上版本，Mysql 数据库和 Redis

第一步，克隆代码：
```buildoutcfg
git clone git@github.com:guoshijiang/columbus.git
```

第二步，搭建一个 virtualenv：
```buildoutcfg
cd columbus
virtualenv .env
source .env/bin/activate
```

第三步，安装依赖：
```buildoutcfg
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

第四步，数据库migrate：
```buildoutcfg
 python3 manage.py migrate
```
如果你改变数据库结构，请先运行 `python3 manage.py makemigrations`, 然后再运行 `python3 manage.py migrate`

第五步，运行服务：
```buildoutcfg
 python3 manage.py runserver
```

如果你在线上部署，建议使用，supervisor 管理进程，Ng 转发，把静态文件使用 `python3 manage.py collectstatic` 收集到相应的目录。

### 4.有问题联系

如果您使用这套代码，开发搭建过程中有任何问题，可以去问我学院（www.wenwoha.com） 上面找联系方式联系我们，也可以直接加我的微信：LGZAXE


### 5.使用本项目做二次开发的条件

使用本套代码做二次开发，需要把所有的产品加友链。


