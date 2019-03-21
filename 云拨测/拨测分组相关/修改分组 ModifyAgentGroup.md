## 1. 接口描述

域名：

接口：ModifyAgentGroup


## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为ModifyAgentGroup。

### 2.1输入参数

| 参数名称             | 必选   | 类型      | 描述                                       |
| ---------------- | ---- | ------ |  ---------------------------------------- |
| GroupId          | 是    | UInt64    |  拨测分组id                                   |
| GroupName        | 是    | String |  拨测分组名称，最长32字节                            |
| IsDefault        | 是    | UInt64    | 是否为默认分组。取值范围 0 或者 1                      |
| Agents | 是    | Array | Province, Isp 需要成对地进行选择。参数对的取值范围。参见：DescribeAgents 的返回结果。            |
#### 

## 3. 输出参数

无


## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=ModifyAgentGroup
&GroupId=28330
&GroupName=test_group2
&IsDefault=0
&Agents.0.Province=gd
&Agents.0.Isp=cmc
&Agents.1.Province=tj
&Agents.1.Isp=cuc
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