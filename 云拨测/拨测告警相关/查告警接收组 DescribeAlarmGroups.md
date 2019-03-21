## 1. 接口描述

域名：

接口：DescribeAlarmGroups



查询用户的告警接收组列表

## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为DescribeAlarmGroups。

### 2.1输入参数

| 参数名称 | 必选   | 类型   | 描述    |
| ---- | ---- | ---- |  ----- |
| Offset | 否    | UInt64  | 满足条件的第几条开始 |
| Limit  | 否    | UInt64  | 每批多少条 |
#### 

## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| TotalCount    | UInt64    | 用户名下总的告警接收组数目 |
| AlarmGroupInfos | AlarmGroupInfo | 满足条件的告警接收组列表                |


## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=DescribeAlarmGroups
&Offset=0
&Limit=2
&<公共请求参数>
```

输出

```
{
	"Response": 
        {	
              "TotalCount": 5,
             "AlarmGroupInfos": [
             {
                "GroupId": 9063,
                "GroupName": "消息分组1",
                "Channel": 3,
                "Remark": null,
                "CreateTime": "2016-01-05 14:41:18"
             },
             {
                "GroupId": 16310,
                "GroupName": "aaa",
                "Channel": 3,
                "Remark": "bbb",
                "CreateTime": "2016-11-01 16:42:40"
              }
              ],
              "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```