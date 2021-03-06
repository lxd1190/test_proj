# 云监控运维端用户操作手册

## 1. 概述
云监控作为统一监控平台，底层barad提供了统一数据上报、接入、存储，上层云监控产品，提供基础设施（物理服务器、网络设备）和各云产品的展示和告警服务。主要有如下功能：

![](/docfile/BCM/UM001.png)


## 2. 监控展示
数据接入barad后，各个云产品的控制台页面，可以调用barad后台的数据进行绘图展示，如物理服务器、网络设备、云服务器、负载均衡、私有网络等云产品的数值指标数据。

### 2.1 云服务器的性能指标展示

![](/docfile/BCM/UM002.png)

![](/docfile/BCM/UM003.png)

### 2.2 物理服务器的性能指标展示

![](/docfile/BCM/UM004.png)

![](/docfile/BCM/UM005.png)



### 2.3 网络设备的性能指标展示
网络设备由于展示维度比较特殊，分整机和端口维度，所以没有整合到云监控产品页面，需要在“基础设施（DCOS）”的网络设备管理页面进行查看。

### 2.3.1 进入网络设备管理页面

![](/docfile/BCM/UM006.png)

### 2.3.2 进入网络设备详情页

![](/docfile/BCM/UM007.png)


### 2.3.3 查看网络设备整机性能监控

![](/docfile/BCM/UM008.png)



### 2.3.4 查看网络设备端口流量监控
![](/docfile/BCM/UM009.png)

### 2.3.5 查看网络设备端口质量监控

![](/docfile/BCM/UM010.png)

### 2.4 CLB LD的性能指标展示

### 2.4.1 进入CLB LD管理页面
![](/docfile/BCM/UM011.png)

### 2.4.2 查看七层LD的性能指标

![](/docfile/BCM/UM012.png)

### 2.4.3 查看四层LD的性能指标

![](/docfile/BCM/UM013.png)

### 2.5 VPC网关集群的性能指标展示

### 2.5.1 VPC网关集群的性能指标

![](/docfile/BCM/UM014.png)

![](/docfile/BCM/UM015.png)


### 2.5.2 NAT网关集群的性能指标


![](/docfile/BCM/UM016.png)


![](/docfile/BCM/UM015.png)

### 2.5.3 JNS网关集群的性能指标


![](/docfile/BCM/UM017.png)


![](/docfile/BCM/UM015.png)



## 3. 事件查询

### 3.1 产品事件查询

![](/docfile/BCM/UM018.png)


### 3.2 根据不同条件进行查询

![](/docfile/BCM/UM019.png)

### 3.3 自定义展示字段

![](/docfile/BCM/UM020.png)

### 3.4 新增和查看事件的告警策略

![](/docfile/BCM/UM021.png)


## 4. 告警管理

### 4.1 告警策略列表查看

![](/docfile/BCM/UM022.png)

### 4.2 点击告警策略，进入详情页

![](/docfile/BCM/UM023.png)

![](/docfile/BCM/UM024.png)

### 4.3  新增告警策略

#### 4.3.1 选择策略类型

![](/docfile/BCM/UM025.png)

#### 4.3.2 定义告警策略（阀值告警）

![](/docfile/BCM/UM026.png)

选择需要告警的具体指标，以及触发条件和抑制条件。

#### 4.3.3 定义告警策略（事件告警）


![](/docfile/BCM/UM027.png)


![](/docfile/BCM/UM028.png)



选择需要告警的具体指标，以及触发条件和抑制条件。

#### 4.3.4 关联告警对象
![](/docfile/BCM/UM029.png)

#### 4.3.5 设置告警接收组

![](/docfile/BCM/UM030.png)

### 4.4 告警信息查询 

#### 4.4.1 告警信息查询

![](/docfile/BCM/UM031.png)


#### 4.4.2 根据策略类型筛选告警列表
![](/docfile/BCM/UM032.png)

## 5. 网络设备日志关键字管理 
网络设备日志关键字管理，主要是用于登记哪些关键字需要进行告警，关联哪些网络设备。

### 5.1 网络设备告警关键字列表页 

![](/docfile/BCM/UM033.png)

### 5.2 新增网络设备告警关键字 
![](/docfile/BCM/UM034.png)

选择关联的网络设备条件，添加关键字、日志类型等信息。后续如果对应的网络设备日志中，发现有填写的关键字，则会触发一个日志告警。

### 5.3 网络设备告警关键字删除 

![](/docfile/BCM/UM035.png)




