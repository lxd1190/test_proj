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


#### 3.5 nws巡检

1. 连接管控barad的DB节点（默认mysql -hbarad.mysql -umysql_user -pmysql_passwd），进入数据库（use BaradNwsStat;）。

2. 查询最近的nws上报统计信息（select * from dNwsDataStat order by logTime desc limit 25;），检查code字段是否存在非0记录，如果有则说明nws存在异常，可尝试重启nws容器。

#### 3.6 其他模块巡检
其他模块均可依赖gaia的健康检查进行巡检。


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
### 5.1 所有产品都无监控数据
#### 故障现象
租户端或运营端控制台所有产品都看不到监控数据。
#### 故障定位及处理
1. 检查ES集群是否正常部署：
    1. 在pod内curl es1.barad:9200/_cat/health?v，如果集群状态为green则正常：<br>
    ![](/docfile/BCM/OM004.png)<br>
    1. 查看存储表是否正常初始化：curl es1.barad:9200/_metrics，正常应返会viewName index的集合，若报无权限或无该index，则创建集群的初始化参数有问题，开启了鉴权，或集群类型创建的不是ctsdb，需将集群销毁重新创建，具体可参考ctsdb oss部署文档。
    1. 查看建表的时间戳格式是否正常：curl es1.barad:9200/_metric/cvm_device-60,若返回的format为epoch_second则为正常，若为epoch_mills则为异常。如异常需要将该表删掉重建（如管控刚刚拉起，存量数据无需保留的话，可将所以metric删掉后重新执行初始化脚本）。<br> 
    ![](/docfile/BCM/OM005.png)<br>
    1. 如以上都正常，且集群本身运营有一段时间后突然没数据，可查看es存储是否被写满,curl es1.barad:9200/_cat/allocation?v的disk.indices可查看当前已使用的node空间，curl es1.barad:5100/_search/clusters 可以看到对应集群预先分配的node磁盘空间。如已达到分配容量，则需要对ES进行扩容：<br>
    ![](/docfile/BCM/OM006.png)<br>
    ![](/docfile/BCM/OM007.png)<br>
1. 检查zk和kafka是否正常：
    1. 登录zk节点，进入zk安装目录，进入bin目录，执行./zkServer.sh status命令，正常则返回leader或follower。若报错则可能zk未启动，执行ps -ef|grep zookeeper查看zk是否正常拉起。
    1. 若zk正常，则在zk的bin目录下执行./zkCli.sh进入zk的shell（最好在leader节点执行,follower也可以，如果执行命令未响应，可重试几次），然后执行ls /kafka/brokers/ids，正常则会返回所有的kafka节点id，一般为[0,1,2]或[1,2,3]三个节点，若少于3个则可能有部分kafka节点异常，get /kafka/brokers/ids/1可查看具体的kafka node信息,endpoints和host为具体的节点信息,此处的ip需要能被集群内pod访问到。<br>
    ![](/docfile/BCM/OM008.png)<br>
    1. 若有部分kafka节点异常，未出现在上述brokers中，则需要登录kafka节点查看kafka节点是否正常。若endpoints中的ip地址不是外界可以访问的ip，则说明kafka配置有误，需登录kafka节点检查kafka的配置文件server.properties中advertised.host.name是否配置为本机的ip，如果不是，需改为本机ip，然后重启kafka节点，其他节点以此类推。（kafka重启需使用bin目录下的kafka-server-stop.sh和kafka-server-start.sh，重启后ps -ef|grep kafka观察下进程的启动时间是否为当前时间）。
    1. kafka节点异常通常是由于磁盘分区被写满，可在相应节点下执行df -lh查看分区使用率。同时检查kafka配置文件的log.dirs是否配置为容量较大的磁盘目录，检查过期时间配置log.cleanup.policy，log.retention.hours是否太长（正常配置过期时间为3d即可）。<br> 
    ![](/docfile/BCM/OM009.png)<br>
    ![](/docfile/BCM/OM010.png)<br>
    ![](/docfile/BCM/OM011.png)<br>
    1. 若kafka异常后恢复，则需要重启barad-nws和barad-event进程，将barad-nws和barad-event pod删掉重新拉起即可。
1. 查看storm任务是否提交，topo是否正常：
    1. 打开stormui界面，查看有无报错：<br>
    ![](/docfile/BCM/OM012.png)<br>
    1. 若无报错，则点进去Barad_Comm topology：<br>
    ![](/docfile/BCM/OM013.png)<br>
    确认该页面无异常信息，且KafkaSpout和ElasticBolt的Emitted为一个较大的数值，若数值为0或小于1000，则很可能是storm的worker异常，需检查下对应worker的日志。
    1. 若报错nimbus找不到leader，则可能： 
        1. pod间域名不通，需进入一个nimubs容器ping另一个nimbus pod的域名，如域名不通，则可能kube-dns有问题，需检查kube-dns是否正常。
        1. node故障导致nimbus的pod同时重启并调度到其他node，导致nimbus在本地找不到元数据信息，认为自己不是leader，发生该情况只能清空zk上的nimbus信息(可重新执行barad的zk初始化脚本)，然后重启nimbus pod。
    1. 若页面上找不到Barad_Comm或BaradUpdateConf，则代表相应的topo未启动，需要在nimbus pod内重新提交topo任务：进入nimbus pod，执行sh /data/config/topo_init.sh，观察结果如果提交success为1，则正常启动，如果failed为1，则启动失败。启动失败的原因一般有以下几种： 
        1. storm-api没有正常拉起，可在nimbus pod内ps -ef|grep storm-api，查看进程是否存在，如进程不存在，则需要进入/usr/local/services/storm-api目录，执行/bin/start.sh拉起进程（弹性交付已加上监控脚本，理论上会自动拉起）。
        1. nimbus服务不正常。需在stormui上或nimubs的日志目录/data/storm110/logs确认nimbus是否正常。
        1. nimbus连接不上zk（具体原因见第6步）。
    1. 若页面上有Barad_Comm和BaradUpdateConf topology，但是点进去之后emitted为0或者值很小，则可能worker为正常工作，或者worker节点之间通信异常。需挑选一个页面下方Worker Resources里的worker pod，进入查看日志。如Barad_Comm里的业务相关日志位于/data/storm110/logs/Barad_Comm目录，worker进程本身的日志位于/data/storm110/logs/workers-artifacts目录。
    1. 若日志里出现连不上zk的报错，则可能是zk超时导致连接数过多，从而被zk节点拒绝连接（zk默认单个node服务同一来源的ip连接数上限是500）。可在storm-woker内执行netstat -natp|grep 2181|wc -l查看zk连接数，正常情况下应该在100以下，若连接数超过500，则可能有异常。 
        1. 解决办法：执行netstat -natp|grep 2181|awk '{print $7}'|sort|uniq -c|sort -k1 -rn|head -10可以查看连接数过多的进程pid。执行ps -ef|grep $PID，可以在最后一行看到具体的topology名字。 <br>
        ![](/docfile/BCM/OM014.png)<br>
        若真的是zk连接数过多，则需要先kill掉对应的topology，在worker内执行kill -9 $PID或者直接删掉storm-worker的pod，然后重新拉起来。连接数降下来之后，需要进入storm-nimbus pod，然后执行sh /data/config/topo_init.sh重新拉起topo。
        1. 规避措施:发生连接数过多一般是因为storm的zk超时时间设置的过短，公有云默认是9s超时，TCE环境将超时时间增大到了50s，但是storm_restore旁路可能有部分客户未升级，导致出现超时。需check下客户的storm镜像版本是否为最新版本，如果是老版本，建议升级镜像。
#### 故障清除
监控控制台数据恢复正常。
#### 运维经验
1. 部署时严格按照部署文档操作。
2. 加强对ZK，ES，Kafka等支撑组件的监控。
3. 加强对集群负载的监控。

### 5.2 部分产品有数据，部分产品无数据
#### 故障现象
部分产品在控制台可以看到监控数据，部分产品看不到。
#### 故障定位
1. 确认上报方是否上报。
1. 如确实上报，检查上报的时间戳是否当前时间戳，默认超过半小时的时间戳会被丢弃。
1. 如有翻译，则检查翻译配置是否正常，翻译字典表数据是否ok：
	1. 查看barad的数据库，StormDictionary库下对应的表里有没有相应的记录。
	2. 若翻译记录未存在，则：
		1. 如果是cvm和LB，则查看barad-script容器内的barad_sync_server是否正常（ps -ef|grep sync_tool）服务是否正常，配置里的CCDB地址是否正确。
		2. 如果是非cvm产品，则先确认业务方是否上报翻译数据，如果有上报，则查看barad-script容器里的dict_access和dict_sync_tool是否正常（ps -ef|grep tornado_cgi.py, ps -ef|grep translate_tool.py）,如不正常，则查看对应组件的日志(位于/data/log下)。
1. 确认ES建表的时间戳格式是否正常（见上一小节《所有产品都无监控数据》）。
1. 检查统计方式是否配置正确（一般只有新业务接入才会有错）。
1. 排查nws和storm日志（nws日志位于/usr/local/services/barad-nws-1.0/log，storm日志位于/data/storm110/logs）。
#### 故障处理
1. 如上报方未上报，则通知上报方处理。
1. 若翻译组件由于配置错误导致服务异常，则更新配置后重启barad-script容器。
1. 若ES建表错误，则将表删除后重建。
1. 如统计方式有误则更正统计方式。
1. 若有其他错误则根据日志信息进行定位。
#### 故障清除
控制台可以看到监控数据恢复正常。
#### 运维经验
1. 集群的初始化操作一定要做。
1. 配置的管理切记不要搞错。

### 5.3 CVM无监控数据
#### 故障现象
其他产品有监控数据，只有CVM看不到监控数据。
#### 故障定位
1. 在子机上确认agent是否安装，agent位于/usr/local/qcloud/monitor目录下。
1. 若agent已安装，确认agent配置的域名是否正确，域名是否能够正常解析，agent配置位于/usr/local/qcloud/monitor/barad/etc/plugin.ini。
1. 若agent未安装，则检查子机stargate是否正常运行(ps -ef|grep sgagent)，日志是否有报错(/usr/local/qcloud/stargate/logs)。
1. 观察子机agent日志有无报错(/usr/local/qcloud/monitor/barad/log)
#### 故障处理
1. 若agent未安装，则安装agent。
1. 若域名不能解析，则需要加上barad相应域名的解析。
#### 故障清除
在控制台上可以看到CVM的监控数据。

### 5.4 监控数据断点或部分机器无数据
#### 故障现象
监控控制台数据有断点。
#### 故障定位
1. 此类情况一般是storm-worker重启导致部分worker通信有问题导致，具体可查看对应topology的worker日志，如确实为通信问题，在storm-nimbus pod内执行sh /data/config/topo_init.sh重启即可解决。
1. 如果客户业务量较大，上报量较大，则可能导致集群负载过高，从而掉点，具体可参考**《Storm扩容》**小节进行检查和扩容。
1. 如storm-worker正常，则需要检查kafka和ES是否正常。某个kafka节点挂掉或者ES集群状态为非green，或ES集群存储被写满也可能导致数据掉点。
#### 故障处理
1. 如果storm负载过高，则进行扩容worker或者扩容pod。
1. 如果ES集群存储被写满，则进行ES扩容。
#### 故障清除
监控控制台曲线连续，不再出现断点。
#### 运维经验
加强对支撑组件的监控。

### 5.5 所有业务无告警
#### 故障现象
对某些业务配置了告警，而且满足了告警触发的条件，但是控制台的告警列表没有告警信息。
#### 故障定位及处理
1. 查看是否有监控数据，若无监控数据，则先按照《无监控数据排查》进行定位。
1. 若有监控数据但无告警，则可能是告警规则未成功加载，查看StormUI，BaradUpdateConf的topology是否正常启动：
	1. 如未启动，则在storm-nimbus pod内执行sh /data/config/topo_init.sh进行拉起。
	1. 如已启动，则可查看zk上告警的节点配置是否更新，或直接查看storm-worker里BaradUpdateConf的日志是否有报错，如有异常，则进入storm-nimbus尝试重启BaradUpdateConf。
1. 查看AMS日志是否正常(barad-api容器，/data/www/ams/log目录，ams.baradAlarm.log.*)，如有对应的发送日志，则表明告警是触发成功的，需根据AMS的错误日志继续排查。
1. 如果上述都正常，则需要进入storm-worker对应topology的日志目录，一般为/data/storm110/logs/Barad_Comm，然后grep对应告警对象的uniqueId进行排查（uniqueId可在barad的db的StormCloudConf.rApplicationPolicy表里根据groupId进行查询）。
#### 故障清除
控制台告警列表可以看到告警触发的信息，并且能收到告警的短信和邮件。

### 5.6 部分业务无告警
#### 故障现象
有部分产品可以收到告警，部分产品收不到告警。
#### 故障定位及处理
1. 查看是否有监控数据。
1. 查看当前的数据是否满足告警条件和持续时间（有时候可能会出现设置了>0但是实际曲线为0的情况，这种不满足告警条件的不会告警），持续N个周期需要连续N+1个异常点才会告警（例如设置了持续一个周期，则需要有连续的两个满足条件的异常点才会告警）。
1. 查看AMS是否有发送日志(barad-api容器，/data/www/ams/log目录，ams.baradAlarm.log.*)，如果有发送日志，但是有报错，大概率是回调接口请求业务接口报错，需根据具体报错信息排查。
1. 如果AMS无发送日志，则需排查barad-alarm pod内的barad-alarm日志(/usr/local/services/cloud_alarm_v2-1.0/log/cloud_alarm.log)，如日志中没有收到异常点的请求，则是由于Storm未发送异常点导致。可参考《所有业务无告警》进行排查。
#### 故障清除
控制台告警列表可以看到收不到告警的产品告警触发的信息，并且能收到告警的短信和邮件。

### 5.7 存量有告警，新增告警策略无告警
#### 故障现象
存量的告警策略可以收到告警，新增的告警策略收不到告警。
#### 故障定位及处理
大概率为storm的BaradUpdateConf未更新配置到zookeeper。参考《所有业务无告警》进行排查。
#### 故障清除
新增的告警策略能够收到告警。

### 5.8 cvm有数据无告警
#### 故障现象
CVM在控制台上有数据，但是收不到告警。
#### 故障定位及处理
1. 大概率为字典表未正确加载，在isd.barad上，qce/cvm的cvm_device视图下，查看对应uuid的appId是否为改用户的appId，如果appId不是租户的appId，则表明字典表未正常加载：
	1. 查看barad的db，StormDictionary.tDictionary_1表里是否有对应uuid的记录，如果有，则可能是dict_loader未正常加载，需重启barad-nws pod。
	2. 如果db里无对应翻译记录，则可能是barad_sync_server配置的ccdb地址错误，需进入barad-script容器对应服务查看日志(/usr/local/services/barad_sync_server-1.0)和配置文件。
1. 若字典表配置正常，则参考《所有业务无告警》进行排查。
#### 故障清除
对于满足告警条件的CVM，控制台上可以看到CVM的告警信息。

### 5.9 无事件信息
#### 故障现象
某个产品发生了某个事件，但是在事件中心的控制台看不到对应的事件信息。
#### 故障定位及处理
1. 检查业务方是否上报。
2. 检查kafka是否正常：
	1. 查看barad-event容器内的nws_event_front日志（/usr/local/services/nws_event_front-1.0/log）,是否有写kafka失败的日志。如果有超时或发送失败，则可能kafka配置不正确或者未初始化`cm_event` topic，需排查kafka配置和kafka的topic列表，可参考kafka部署文档。
	2. 如果写kafka正常（上报成功，且nws_event_front无错误日志），但是event_handle模块的日志没有消费kafka的日志，则可能kafka该topic异常。可尝试换一个topic进行测试，即在kafka上新建一个topic，然后更新nws_event_front和event_handle的配置文件，替换topic为新的topicName，然后重启这两个服务。
3. 检查ES建表是否正常:`curl es1.barad:9200/_metric/tce_bm_lost_agent`,返回的timestamp的format字段应为epoch_second，如果返回报错或者返回的字段为epoch_mills，则表明未建表或建表异常，需删掉改表并重新建表。
#### 故障清除
在事件中心控制台可以看到新增的事件信息。

### 5.10 有事件无告警
#### 故障现象
事件中心可以看到事件发生，但是告警列表看不到，并且订阅了告警的人员收不到告警信息。
#### 故障定位及处理
1. 即事件中心有记录但告警列表无记录。
1. 查看该事件和对象是否绑定了告警策略，如未配置，则事件中心的记录里会展示**未配置**，该情况为正常情况，如需要告警，则需要在告警策略页面为改事件绑定告警对象。
1. 若事件绑定了告警，但是无告警记录，则需要查看AMS日志进行排查。
#### 故障清除
对于已绑定告警的时间，在控制台告警列表可以看到已发生事件的告警记录，已订阅告警的人员能够收到告警。

### 5.11 有告警无短信和邮件
#### 故障现象
告警列表可以看到告警记录，但是订阅了告警的人员收不到短信和邮件。
#### 故障定位及处理
1. 大概率为消息中心问题。
2. 查看AMS日志(barad-api容器，/data/www/ams/log目录)，查看MessageGroupClass.log.*文件，是否有发送消息中心失败的日志。
3. 若告警记录正常，但无发送日志，则：
	1. 查看该告警策略是否绑定告警接收组，且接收组里的接收人已认证。
	2. 如果是运营端，则查看接收组的ID是否大于10000000，理论上运营端接收组ID都应该大于10000000，如果小于10000000，则联系消息中心同事查看是否消息中心db初始化有问题。
#### 故障清除
对于新发生的事件，已经订阅改告警的人员可以收到短信和邮件提醒。


## 6 扩容
### 6.1 Storm扩容
#### 扩容依据
1. 通过storm ui上的每个component的capacity指标来判断是否存在计算资源不足的情况。Capacity越大说明该component计算资源需要库容，目前参考值为0.6，即Capacity>0.6，表示需要扩容(忽略AlarmBackupBolt)。 <br>
  ![](/docfile/BCM/OM015.png)<br>
1. 在barad的db里查询每分钟的上报量，单个worker的最大处理能力为50w/min，如果当前worker数不能满足，则考虑扩容worker数。8c32g的pod建议的worker数为6个，单个pod的worker数超过6个即考虑扩容pod。```select logTime, sum(nCount) from BaradNwsStat.dNwsDataStat where topoName='Barad_Comm' and logTime > date_sub(now(), interval 10 minute ) group by logTime;```

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