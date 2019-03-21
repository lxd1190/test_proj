## 1. 接口描述

域名：

接口：DescribeAgentGroup


## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为DescribeAgentGroup。

### 2.1输入参数

| 参数名称    | 必选   | 类型      | 描述     |
| ------- | ---- | ---- | ------ |
| GroupId | 是    | UInt64  | 拨测分组id |
#### 

## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| GroupId    | UInt64    | 拨测分组Id |
| GroupName | String | 拨测分组名称               |
| IsDefault    | UInt64  | 是否为默认拨测分组              |
| TaskNum    | UInt64  | 使用本拨测分组的任务数              |
| Agents    | Array  | 拨测分组运营商列表              |


## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=DescribeAlarmGroups
&GroupId=10000888
&<公共请求参数>

```

输出

```
{
	"Response": 
        {	
            "GroupName": "test_group",
            "GroupDesc": "",
            "IsDefault": 0,
            "Agents": [
                {
                    "Province": "gd",
                    "ProvinceName": "广东",
                    "Isp": "ctc",
                    "IspName": "电信"
                },
                {
                    "Province": "gd",
                    "ProvinceName": "广东",
                    "Isp": "cuc",
                    "IspName": "联通"
                }            
            ],
            "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```