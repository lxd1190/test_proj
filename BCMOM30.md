# 云拨测Cat运维手册
## 1 产品介绍
云拨测（Cloud Automated Testing）是依托腾讯专有的服务质量监测网络，利用分布于全球的服务质量监测点，对您的网站、域名、后台接口等进行周期性监控，您可通过查看可用率和延时随时间区间变化来帮助分析站点质量情况。云拨测对可用率指标提供自定义阈值告警功能，您可以通过配置告警实现异常实时通知。可视化性能数据和告警通知可帮助您及时对业务质量作出反应，保证业务稳定正常运行。
## 2 产品架构
![](/docfile/BCM/OM001.png)
## 3 拨测组件巡检
#### 3.1 zookeeper巡检

1. 登录所有zk节点，找到zookeeper安装目录（默认/usr/local/services/zookeeper），进入bin目录，运行./zkServer.sh status 。所有节点无错误输出，除了follower外，有1个leader，则zk集群是运行正常的。

2. 进入bin目录下，运行./zkCli.sh，运行 ls / ，返回的目录中必须有 /storm110，/kafka ， /kfkSpout 。缺失则标明对应的组件存在异常（以上目录对应的组件依次为 storm，kafka，storm）。 

#### 3.2 kafka巡检
1. 登录一台zk机器，找到zookeeper安装目录（默认/usr/local/services/zookeeper）。

2. 进入bin目录下，运行zkCli.sh，运行 ls /kafka/brokers/ids。<br>
如果返回 [1, 2, 3] 则表示有3台kafka节点在运行中，如果缺少，有可能节点有异常，但不一定影响服务，但仍需尽快修复。

#### 3.3 storm巡检
1. 进入到nimbus节点机器。

2. cd /usr/local/services/storm/bin/到此目录下运行./storm list。<br>如果出现下面这些Topology status为ACTIVE,则表明正常。

    **Topology_name        Status     Num_tasks  Num_workers  Uptime_secs**<br>
UpdateConf           ACTIVE     4          1            365484    
NWS_CAT1           ACTIVE     338         32            365513    


## 4 故障处理思路
### 数据链路
![](/docfile/BCM/OM002.png)
### 定位流程
![](/docfile/BCM/OM003.png)
### 排查思路
1. 分析具体场景，缩小范围。
2. 针对具体case分析。
3. 全链路分析。

## 5 故障处理CASE
### 5.1 监控数据未写入CDB
#### 故障现象
API拉不到监控数据或在CDB中无法看到上报数据
#### 故障定位及处理
1. 检查zk和kafka是否正常：
    1. 登录zk节点，进入zk安装目录，进入bin目录，执行./zkServer.sh status命令，正常则返回leader或follower。若报错则可能zk未启动，执行ps -ef|grep zookeeper查看zk是否正常拉起。
    1. 若zk正常，则在zk的bin目录下执行./zkCli.sh进入zk的shell（最好在leader节点执行,follower也可以，如果执行命令未响应，可重试几次），然后执行ls /kafka/brokers/ids，正常则会返回所有的kafka节点id，一般为[0,1,2]或[1,2,3]三个节点，若少于3个则可能有部分kafka节点异常，get /kafka/brokers/ids/1可查看具体的kafka node信息,endpoints和host为具体的节点信息,此处的ip需要能被集群内pod访问到。<br>
    ![](/docfile/BCM/OM008.png)<br>
    1. 若有部分kafka节点异常，未出现在上述brokers中，则需要登录kafka节点查看kafka节点是否正常。若endpoints中的ip地址不是外界可以访问的ip，则说明kafka配置有误，需登录kafka节点检查kafka的配置文件server.properties中advertised.host.name是否配置为本机的ip，如果不是，需改为本机ip，然后重启kafka节点，其他节点以此类推。（kafka重启需使用bin目录下的kafka-server-stop.sh和kafka-server-start.sh，重启后ps -ef|grep kafka观察下进程的启动时间是否为当前时间）。
    1. kafka节点异常通常是由于磁盘分区被写满，可在相应节点下执行df -lh查看分区使用率。同时检查kafka配置文件的log.dirs是否配置为容量较大的磁盘目录，检查过期时间配置log.cleanup.policy，log.retention.hours是否太长（正常配置过期时间为3d即可）。<br> 
    ![](/docfile/BCM/OM009.png)<br>
    ![](/docfile/BCM/OM010.png)<br>
    ![](/docfile/BCM/OM011.png)<br>
1. 查看storm任务是否提交，topo是否正常：
    1. 打开stormui界面，查看有无报错：<br>
    ![](/docfile/BCM/OM012.png)<br>
    1. 若无报错，则点进去NWS_CAT1 topology：<br>
    ![](/docfile/BCM/OM013.png)<br>
    确认该页面无异常信息，且KafkaSpout的Emitted为一个较大的数值，若数值为0或小于1000，则很可能是storm的worker异常，需检查下对应worker的日志。
    1. 若报错nimbus找不到leader，则可能： 
        1. pod间域名不通，需进入一个nimubs容器ping另一个nimbus pod的域名，如域名不通，则可能kube-dns有问题，需检查kube-dns是否正常。
        1. node故障导致nimbus的pod同时重启并调度到其他node，导致nimbus在本地找不到元数据信息，认为自己不是leader，发生该情况只能清空zk上的nimbus信息(可重新执行barad的zk初始化脚本)，然后重启nimbus pod。
    1. 若页面上找不到NWS_CAT1或UpdateConf，则代表相应的topo未启动，需要在nimbus pod内重新提交topo任务：进入nimbus pod，执行sh /data/config/topo_init.sh，观察结果如果提交success为1，则正常启动，如果failed为1，则启动失败。启动失败的原因一般有以下几种： 
        1. storm-api没有正常拉起，可在nimbus pod内ps -ef|grep storm-api，查看进程是否存在，如进程不存在，则需要进入/usr/local/services/storm-api目录，执行/bin/start.sh拉起进程（弹性交付已加上监控脚本，理论上会自动拉起）。
        1. nimbus服务不正常。需在stormui上或nimubs的日志目录/data/storm110/logs确认nimbus是否正常。
        1. nimbus连接不上zk（具体原因见第6步）。
    1. 若页面上有NWS_CAT1和UpdateConf topology，但是点进去之后emitted为0或者值很小，则可能worker为正常工作，或者worker节点之间通信异常。需挑选一个页面下方Worker Resources里的worker pod，进入查看日志。
    1. 若日志里出现连不上zk的报错，则可能是zk超时导致连接数过多，从而被zk节点拒绝连接（zk默认单个node服务同一来源的ip连接数上限是500）。可在storm-woker内执行netstat -natp|grep 2181|wc -l查看zk连接数，正常情况下应该在100以下，若连接数超过500，则可能有异常。 
        1. 解决办法：执行netstat -natp|grep 2181|awk '{print $7}'|sort|uniq -c|sort -k1 -rn|head -10可以查看连接数过多的进程pid。执行ps -ef|grep $PID，可以在最后一行看到具体的topology名字。 <br>
        ![](/docfile/BCM/OM014.png)<br>
        若真的是zk连接数过多，则需要先kill掉对应的topology，在worker内执行kill -9 $PID或者直接删掉storm-worker的pod，然后重新拉起来。连接数降下来之后，需要进入storm-nimbus pod，然后执行sh /data/config/topo_init.sh重新拉起topo。
        1. 规避措施:发生连接数过多一般是因为storm的zk超时时间设置的过短，公有云默认是9s超时，TCE环境将超时时间增大到了50s，但是storm_restore旁路可能有部分客户未升级，导致出现超时。需check下客户的storm镜像版本是否为最新版本，如果是老版本，建议升级镜像。
#### 运维经验
1. 部署时严格按照部署文档操作。
2. 加强对ZK，Kafka等支撑组件的监控。
3. 加强对集群负载的监控。

## 6 扩容
### 6.1 Storm扩容
#### 扩容依据
1. 通过storm ui上的每个component的capacity指标来判断是否存在计算资源不足的情况。Capacity越大说明该component计算资源需要库容，目前参考值为0.6，即Capacity>0.6，表示需要扩容(忽略AlarmBackupBolt)。 <br>
  ![](/docfile/BCM/OM015.png)<br>

#### 扩容操作
1. Storm topology的资源配置是在配置中心中的storm模块设置的，因此可以调整这些配置项，然后重启相应的topology即可，注意：这里修改topology资源配置后，重启该topology才能生效。<br>
  ![](/docfile/BCM/OM016.png)<br>
1. 在配置中心中找到需要调整的topology资源配置项，如Barad_Comm.resource.config。
1. 点击后面的“编辑”，修改workerNum或者spout/bolt的资源数,workerNum与spout/bolt资源数的比例关系可以参考下表（workerNum与Spout/Bolt资源数的比例，假设workNum=N）。编辑后点击保存。
   
    |Spout/Bolt|	Task数（N为workerNum数）|
	|-------|---------|
	|KafkaSpout|	topic partition数，无workerNum无关|
	|AccessBolt|	2N|
	|StatBolt|	3N|
	|LogBolt|	1/2 N|
	|AlarmBolt|	N|
	|PolicySyncSpout|	32（恒定值）|
	|TickSpout|	1（恒定值）|
    示例说明：
  	1. Barad_Comm.resource.config：表示Barad_Comm这个topology的资源配置项。		 
  	1. 	{"workerNum":8,"TickSpout":1,"AccessBolt":16,"StatBolt":24,"LogBolt":4,"StorageBolt":8,"MysqlBolt":0,"HBaseBolt":16,"AlarmBolt":8,"KafkaSpout":8,"PolicySyncSpout":32,"debugMode":0,"ElasticBolt":16}，其中: 
        workerNum:8 表示Barad_Comm这个topology的worker数为8个
        AccessBolt:16表示AccessBolt的task数（线程数）为16个。
        StatBolt:24表示StatBolt的task数（线程数）为16个。
1. 重启该topology生效，重启步骤：登录到一台nimbus pod，cd /usr/local/service/storm-api-tools，执行python tool.py restart –region xx –topology xx –version xx –operator xx (可参考nimbus pod里/data/config/topo_init.sh脚本)

### 6.2 其他POD扩容
#### 扩容依据
除去ZK，Kafka，ES为物理机部署，Barad-Storm为有状态服务外，Barad其他组件均为无状态服务，已全部容器化部署，只需根据资源使用率进行扩容即可：

 - 当资源使用率大于**80%**需进行扩容
 - 由于负载过高导致pod频繁重启需进行扩容
#### 扩容操作
1. 在gaia页面上进行自动扩缩容。
1. 同时修改部署yaml的replica个数。