## 1. 接口描述

域名：

接口：GetCatReturnCodeHistory



查询拨测任务的历史返回码信息

## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为GetCatReturnCodeHistory。

### 2.1输入参数

| 参数名称      | 必选   | 类型       | 描述                                       |
| --------- | ---- | ------ | ---------------------------------------- |
| TaskId    | 是    | UInt64    | 拨测任务id  | 正整数。验证成功的拨测任务id                          |
| BeginTime | 是    | String | 告警的起始时间 | 开始时间点。格式如：2017-05-09 10:20:00                 |
| EndTime   | 是    | String | 告警的截至时间 | 结束时间点。格式如：2017-05-09 10:25:00                 |
| Province  | 是    | String | 省份      | 省份名称的全拼 |
#### 

## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| Details    | Array    | 错误码, 0: 成功, 其他值表示失败 |
| Summarys | Array | 返回信息                |
| BeginTime    | DateTime  | 结果数据                |
| EndTime    | DateTime  | 结果数据                |

## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=GetReturnCodeHistory
&TaskId=185553
&BeginTime=2018-04-20 15:51:00
&EndTime=2018-04-20 16:51:00
&Province=gd
&<公共请求参数>
```

输出

```
{
    "Response": {
        "Details": [
            {
                "IspName": "移动",
                "Province": "gd",
                "ProvinceName": "广东",
                "MapKey": "guangDong",
                "ServerIp": "10.185.9.80",
                "ResultCount": 14,
                "ResultCode": 10020,
                "ErrorReason": "禁止内网ip拨测"
            },
            {
                "IspName": "移动",
                "Province": "gd",
                "ProvinceName": "广东",
                "MapKey": "guangDong",
                "ServerIp": "NULL",
                "ResultCount": 49,
                "ResultCode": 10020,
                "ErrorReason": "禁止内网ip拨测"
            },
            {
                "IspName": "电信",
                "Province": "gd",
                "ProvinceName": "广东",
                "MapKey": "guangDong",
                "ServerIp": "10.185.9.80",
                "ResultCount": 14,
                "ResultCode": 10020,
                "ErrorReason": "禁止内网ip拨测"
            },
            {
                "IspName": "联通",
                "Province": "gd",
                "ProvinceName": "广东",
                "MapKey": "guangDong",
                "ServerIp": "10.185.9.80",
                "ResultCount": 13,
                "ResultCode": 10020,
                "ErrorReason": "禁止内网ip拨测"
            },
            {
                "IspName": "其他",
                "Province": "gd",
                "ProvinceName": "广东",
                "MapKey": "guangDong",
                "ServerIp": "10.185.9.80",
                "ResultCount": 14,
                "ResultCode": 10020,
                "ErrorReason": "禁止内网ip拨测"
            }
        ],
        "Summary": [
            {
                "ResultCount": 104,
                "ErrorReason": "禁止内网ip拨测",
                "ResultCode": 10020
            }
        ],
        "BeginTime": "2018-04-20 15:51:00",
        "EndTime": "2018-04-20 16:51:00",
        "RequestId": "6b9fd810-c2a5-413d-ac23-a5a42eaf1471"
    }
}
```