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
https://catapi.api.qcloud.com/v2/index.php?
& <<a href="https://cloud.tencent.com/doc/api/229/6976">公共请求参数</a>>
&Action=DescribeAlarmGroups
&page=1
&num=2
```

输出

```
{
    "code": 0,
    "message": "",
    "codeDesc": "Success",
    "total": 2,
    "alarmGroupInfo": [
        {
            "groupId": 9063,
            "groupName": "消息分组1",
            "channel": 3,
            "remark": null,
            "createTime": "2016-01-05 14:41:18"
        },
        {
            "groupId": 16310,
            "groupName": "aaa",
            "channel": 3,
            "remark": "bbb",
            "createTime": "2016-11-01 16:42:40"
        }
    ]
}
```