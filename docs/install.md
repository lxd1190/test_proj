## 安装文档

# 目录
> * [手工安装说明](#chapter-1)
>> * [依赖环境](#chapter-1-1)
>> * [数据库环境安装](#chapter-1-2)
>> * [服务端环境安装](#chapter-1-3)
>> * [WEB管理端环境安装](#chapter-1-4)
>
> * [docke部署](#chapter-5)
> 
本安装文档仅描述了在一台服务器上安装搭建整个Metis的过程，目的是为了让用户对Metis的部署搭建、运行等整体认识。

如要用于生产环境，需要更多考虑分布式系统下容错、容灾能力。若有需要，可以加入Metis的qq技术交流群：288723616。

#1. <a id="chapter-1"></a>手工安装
## 1.1. <a id="chapter-1-1"></a>依赖环境

| 软件  | 软件要求 |
| ---  | ---  |
| linux内核版本:| CentOS 7.4 |
| python版本:| 2.7版本|
| mysql版本:| 5.6.26及以上版本|
| Node.js版本:| 8.11.1及以上版本|s
| Django版本:| 1.11.13及以上版本|

运行服务器要求：1台普通安装linux系统的机器即可（推荐CentOS系统）。2.服务器需要开放80和8080端口

以下步骤假定安装机器的代码目录是 `/data/Metis/`，可根据实际情况更改。

## 1.2. <a id="chapter-1-2"></a>数据库环境安装

### 1.2.1. mysql 安装介绍

采用yum源安装或者在mysql官网下载源码安装，安装好后检测mysql服务是否正常工作。

```
yum install mariadb-server
systemctl start mariadb
```

### 1.2.2. 初始化数据库

为了方便用户快速使用，提供了50+异常检测结果数据和300+样本数据供大家使用。

1、创建需要的数据库用户名并授权，连接mysql客户端并执行

```
   grant all privileges on *.* to metis@127.0.0.1  identified by 'metis@123';
   flush privileges;
```
   
2、创建数据库 `metis`，在命令行下执行

```
mysqladmin -umetis -pmetis@123 -h127.0.0.1 create metis
```

3、将`/Metis/app/sql/`目录下的sql初始化文件，导入数据`metis`数据库

```
mysql -umetis -pmetis@123 -h127.0.0.1 metis < /data/Metis/app/sql/time_series_detector/anomaly.sql
mysql -umetis -pmetis@123 -h127.0.0.1 metis < /data/Metis/app/sql/time_series_detector/sample_dataset.sql
mysql -umetis -pmetis@123 -h127.0.0.1 metis < /data/Metis/app/sql/time_series_detector/train_task.sql
```

4、将数据库配置信息更新到服务端配置文件`database.py`
```
vim /data/Metis/app/config/database.py
```
改写配置
```
db = 'metis'
user = 'metis'
passwd = 'metis@123'
host = '127.0.0.1'
port = 3306
```

## 1.3. <a id="chapter-1-3"></a>服务端环境安装

服务端python程序需要依赖django、numpy、tsfresh、MySQL-python、scikit-learn、scikit-learn等包

### 1.3.1. yum 安装依赖包

```
yum install python-pip
pip install --upgrade pip
yum install gcc libffi-devel python-devel openssl-devel
yum install mysql-devel
```

### 1.3.2. pip 安装python依赖包

通过工程目录下requirements.txt安装

```
pip install -I -r requirements.txt
```

### 1.3.3. 工作目录加入环境变量

```
export PYTHONPATH=/data/Metis:$PYTHONPATH
```

为了保证下次登陆可以导入环境变量,请将环境变量配置写入/etc/profile文件

### 1.3.4. 部署Django服务端

部署生产环境时可通过nginx和uwsgi部署，具体请参考对应官网说明

### 1.3.5. 启动服务端

启动服务端程序

```
python /data/Metis/app/controller/manage.py runserver {ip}:{port}
```

## 1.4. <a id="chapter-1-4"></a>WEB管理端环境安装

### 1.4.1. Node.js安装

需先安装[Node.js](https://nodejs.org/en/download/)，并且Node.js的版本需不低于 8.11.1

### 1.4.2. npm install安装前端依赖

安装 pacakge.json 配置文件中依赖的第三方安装包

### 1.4.3. 编译代码

修改uweb/src/app.json 文件的后端地址配置: "origin": "http://${ip}:${port}" , ip和port对应服务端地址

运行npm run build

将uweb目录下的custom文件夹下复制到uweb目录下生成的dist文件夹中

将nginx配置文件中的root定位到uweb目录下的dist文件夹

nginx配置如下：

```
server {
        listen       80;
        root /*/uweb/dist;
        location / {
                add_header Cache-Control max-age=0;
                gzip on;
                gzip_min_length 1k;
                gzip_buffers 16 64k;
                gzip_http_version 1.1;
                gzip_comp_level 6;
                gzip_types text/plain application/x-javascript text/css application/xml;
                gzip_vary on;
                    try_files $uri $uri/ /index.html;
        }

        location /index.html {
                add_header Cache-Control 'no-store';
        }
    }
```

### 1.4.4. 启动WEB服务

nginx正常启动后，打开浏览器并访问 http://${ip}:80/

### 1.4.5. 本地修改调试

如本地修改代码，发布更新方式如下：

npm run build 项目代码开发完成后，执行该命令打包项目代码。在项目根目录会生成一个 dist 目录，然后复制custom目录，放至dist目录下。发布时，将 dist 目录中的全部文件作为静态文件，放至服务器指定的静态文件目录即可

# 5. <a id="chapter-5"></a>docker方式部署

## 5.1. 安装docker

```
yum install docker
service docker start
```

## 5.2. 部署docker环境
执行Meits/docker/start.sh ${本机ip},等待部署完成

部署完成后,可以通过浏览器直接访问:http://${IP}



