## 1. 接口描述

域名：

接口：ModifyAlarmPloicy



## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为ModifyAlarmPloicy。

### 2.1输入参数

| 参数名称            | 必选   | 类型     | 描述                                       |
| --------------- | ---- | ------ | ---------------------------------------- |
| TaskId        | 是    | UInt64    | 验证成功的拨测任务id                                 |
| Interval      | 是    | UInt64    | 持续周期。值为任务的Period 乘以0、1、2、3、4。单位：分钟                                     |
| Operate       | 是    | String    | 目前取值仅支持 lt (小于)       |
| Threshold     | 是    | UInt64 | 门限百分比。比如：80，表示80%。成功率低于80%时告警                          |
| PolicyId      | 是    | UInt64    | 拨测告警策略id           |
| ReceiverGroupId | 是    | UInt64    | 告警接收组的id。参见： DescribeAlarmGroups 接口。从返回结果里的GroupId 中选取一个 |
#### 

## 3. 输出参数

无

## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=UpdateAlarmPolicy
&TaskId=24418
&PolicyId=28330
&Interval=1
&Operate=lt
&Threshold=70
&ReceiverGroupId=1513
&<公共请求参数>
```

输出

```
{
	"Response": 
        {	
               "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```