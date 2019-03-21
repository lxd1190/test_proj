## 1. 接口描述

域名：

接口：CreateAgentGroup


## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为CreateAgentGroup。

### 2.1输入参数

| 参数名称             | 必选   | 类型      | 描述                                       |
| ---------------- | ---- | ------ | ---------------------------------------- |
| GroupName        | 是    | String | 拨测分组名称                           |
| IsDefault        | 是    | UInt64    | 是否为默认分组                  |
| Agents| 是    | CatAgent数组 | Province, Isp 需要成对地进行选择。参数对的取值范围。参见：DescribeAgentList 的返回结果。           |

#### 

## 3. 输出参数

| 参数名称    | 类型       | 描述                  |
| ------- | -------- | ------------------- |
| GroupId | UInt64 | 拨测分组id              |


## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=CreateAgentGroup
&GroupName=test_group2
&IsDefault=0
&Agents.0.province=gd
&Agents.0.isp=cmc
&Agents.1.province=gd
&Agents.1.isp=cuc
&<公共请求参数>
```

输出

```
{
	"Response": 
        {	
               "GroupId": 28330,
               "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```