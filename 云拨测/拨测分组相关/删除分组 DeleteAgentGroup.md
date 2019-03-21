## 1. 接口描述

域名：

接口：DeleteAgentGroup


## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为DeleteAgentGroup。

### 2.1输入参数

| 参数名称    | 必选   | 类型     | 描述     |
| ------- | ---- | ---- | ------ |
| GroupId | 是    | UInt64  |  拨测分组id |
#### 

## 3. 输出参数

           
## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=DeleteAgentGroup
&GroupId=28330
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