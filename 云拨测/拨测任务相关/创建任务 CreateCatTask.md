## 1. 接口描述

域名：

接口：CreateTaskEx



创建或修改 拨测任务。
如果验证未成功，请先验证成功。避免创建失败率100%的拨测任务。对于已存在的任务id，会执行修改操作。


## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为CreateTaskEx。

### 2.1输入参数

| 参数名称         | 必选   | 类型      | 描述                                       |
| ------------ | ---- | ------ | ---------------------------------------- |
| AgentGroupId | 否    | UInt64 | 拨测分组id，体现本拨测任务要采用那些运营商作为拨测源。一般可直接填写本用户的默认拨测分组。参见：DescribeAgentGroupList 接口，本参数使用返回结果里的groupId的值。                         |
| CatTypeName  | 是    | String | http, https, ping, tcp, ftp, smtp, udp, dns 之一 |
| Url          | 是    | String | 拨测的url  例如：www.baidu.com (url域名解析需要能解析出具体的ip)               |
| Host         | 否    | String | 指定域名(如需要)   |
| IsHeader     | 否    | UInt64 | 是否为Header请求（非0 发起Header 请求。为0，且PostData 非空，发起POST请求。为0，PostData 为空，发起GET请求）                           |
| SslVer       | 是    | Int    | url中含有https时有用。缺省为SSLv23。需要为 TLSv1_2, TLSv1_1, TLSv1, SSLv2, SSLv23, SSLv3 之一 |
| PostData     | 否    | String | POST 请求数据。空字符串表示非POST请求               |
| UserAgent    | 否    | String | 用户agent 信息  |
| CheckStr     | 否    | String | 要在结果中进行匹配的字符串   |
| CheckType    | 否    | String | 1 表示通过检查结果是否包含CheckStr 进行校验   |
| Cookie       | 否    | String | 需要设置的cookie信息  |
| Period       | 否    | UInt64 | 拨测周期。取值可为1,5,15,30之一, 单位：分钟。精度不能低于用户等级规定的最小精度   |
| TaskName     | 是    | String | 拨测任务名称不能超过32个字符。同一个用户创建的任务名不可重复   |
| TaskId       | 否    | UInt64 | 任务号。用于验证且修改任务时传入原任务号   |
| UserName     | 否    | String | 登陆服务器的账号。如果为空字符串，表示不用校验用户密码。只做简单连接服务器的拨测。  |
| PassWord     | 否    | String | 登陆服务器的密码   |
| ReqDataType  | 否    | UInt64 | 缺省为0。0 表示请求为字符串类型。1表示为二进制类型  |
| ReqData      | 否    | String | 发起tcp, udp请求的协议请求数据   |
| RespDataType | 否    | UInt64 | 缺省为0。0 表示请求为字符串类型。1表示为二进制类型   |
| RespData     | 否    | String | 预期的udp请求的回应数据。字符串型，只需要返回的结果里包含本字符串算校验通过。二进制型，则需要严格等于才算通过  |
| DnsSvr       | 否    | String | 目的dns服务器  可以为空字符串  |
| DnsCheckIp   | 否    | String | 需要检验是否在dns ip列表的ip。可以为空字符串，表示不校验   |
| DnsQueryType | 否    | String | 需要为下列值之一。缺省为A。A, MX, NS, CNAME, TXT, ANY   |
| UseSecConn   | 否    | UInt64 | 是否使用安全链接ssl  0 不使用，1 使用   |
| NeedAuth     | 否    | UInt64 | ftp登陆验证方式  0 不验证  1 匿名登陆  2 需要身份验证   |
| Port         | 否    | UInt64 | 拨测目标的端口号  |
| Type         | 否    | UInt64 | Type=0 默认 （站点监控）Type=2 可用率监控  |




## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| ResultId    | UInt64    | 拨测结果查询id。接下来可以使用查询拨测是否能够成功，验证能否通过。 |
| TaskId | UInt64 | 拨测任务id。验证通过后，创建任务时使用，传递给CreateTask 接口。                |


## 4. 错误码表

| 错误代码  | 错误描述                                | 英文描述                          |
| ----- | ----------------------------------- | ----------------------------- |
| 10001 | 输入参数错误。可能是达到最大拨测分组数限制。结合message一起看。 | InvalidParameter              |
| 11000 | DB操作失败                              | InternalError.DBoperationFail |
| 20004 | 调用teg拨测服务失败                         | InternalError                 |

## 5. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=CreateTaskEx
&CatTypeName=http
&Period=5
&AgentGroupId=1510
&Url=www.tencent.com
&TaskName=test_http
&<公共请求参数>
```

输出

```
{
	"Response": 
        {	
               "ResultId": 28330,
               "TaskId": 24454,
               "RequestID": "6de91190-a148-97a4-a935-f44cf51e1d61"
	}	
}
```