## 1. 接口描述

域名：

接口：DescribeTasks



查询拨测任务列表

## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为DescribeCatTaskList。

### 2.1输入参数

| 参数名称   | 必选   | 类型    | 描述                    |
| ------ | ---- | ---- |  --------------------- |
| offset | 否    | UInt64  | 从第offset 条开始查询。缺省值为0  |
| limit  | 否    | UInt64  | 本批次查询limit 条记录。缺省值为20 |
| GroupId  | 否    | UInt64  | 任务所使用的拨测分组Id |
#### 

## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| TotalCount    | UInt64    | 用户的拨测任务总条数 |
| Tasks | CatTask数组 | 满足条件的拨测任务列表                |

##### 


## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=DescribeTasks
&Offset=0
&Limit=2
&<公共请求参数>
```

输出

```
{
	"Response": 
        {	
            "TotalCount":10,
            "Tasks": [
            {
                "TaskId": 24418,
                "AppId": 1251342139,
                "TaskName": "keke_test_pop3",
                "CgiUrl": "pop.qq.com",
                "CatTypeName": "pop3",
                "Status": 2,
                "Period": 5,
                "AvailRatioThres": 90,
                "AvailRatioInterval": 15,
                "ReceiverGroupId": 9063,
                "AddTime": "2017-05-10 17:29:15",
                "UpdateTime": "2017-05-11 15:44:20",
                "AgentGroupId": 1050
            },
            {
                "TaskId": 24420,
                "AppId": 1251342139,
                "TaskName": "test_ftp_keke2",
                "CgiUrl": "115.159.142.79",
                "CatTypeName": "ftp",
                "Status": 2,
                "Period": 5,
                "AvailRatioThres": null,
                "AvailRatioInterval": null,
                "ReceiverGroupId": null,
                "AddTime": "2017-05-11 14:38:38",
                "UpdateTime": "2017-05-19 15:15:59",
                "AgentGroupId": 1051
            }
            ],
            "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```