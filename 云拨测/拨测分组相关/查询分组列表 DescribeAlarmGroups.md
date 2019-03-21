## 1. 接口描述

域名：
接口：DescribeAgentGroups



查询当前用户的所有拨测分组列表

## 2. 输入参数

以下请求参数列表仅列出了接口请求参数，正式调用时需要加上公共请求参数，见<a href="/doc/api/405/公共请求参数" title="公共请求参数">公共请求参数</a>页面。其中，此接口的Action字段为DescribeCatAgentGroupList。

### 2.1输入参数

| 参数名称 | 必选   | 类型   | 输入内容 | 描述   |
| ---- | ---- | ---- | ---- | ---- |
| 无    |      |      |      |      |
#### 

## 3. 输出参数

| 参数名称    | 类型     | 描述                  |
| ------- | ------ | ------------------- |
| SysDefaultGroup    | AgentGroup    | 用户所属的系统默认拨测分组 |
| CustomGroups | AgentGroup数组 | 用户创建的拨测分组列表          |

## 4. 示例

输入

```
https://cat.tencentcloudapi.com/?Action=DescribeAgentGroups
&<公共请求参数>

```

输出

```
{
    "Response": {
        "SysDefaultGroup": {
            "GroupId": 100000003,
            "GroupName": "免费用户默认组",
            "IsDefault": 1,
            "MaxGroupNum": 5,
            "TaskNum": 0,
            "GroupDetail": [
                {
                    "Isp": "ctc",
                    "IspName": "电信",
                    "Province": "zj",
                    "ProvinceName": "浙江"
                },
                {
                    "Isp": "cmc",
                    "IspName": "移动",
                    "Province": "sh",
                    "ProvinceName": "上海"
                },
                {
                    "Isp": "ctc",
                    "IspName": "电信",
                    "Province": "gd",
                    "ProvinceName": "广东"
                },
                {
                    "Isp": "cuc",
                    "IspName": "联通",
                    "Province": "tj",
                    "ProvinceName": "天津"
                },
                {
                    "Isp": "ctc",
                    "IspName": "电信",
                    "Province": "sx",
                    "ProvinceName": "陕西"
                }
            ]
        },
        "CustomGroups": [
            {
                "GroupId": 100003502,
                "GroupName": "test_group88",
                "TaskNum": 1,
                "IsDefault": 0,
                "GroupDetail": [
                    {
                        "Isp": "cmc",
                        "IspName": "移动",
                        "Province": "gd",
                        "ProvinceName": "广东"
                    },
                    {
                        "Isp": "cuc",
                        "IspName": "联通",
                        "Province": "tj",
                        "ProvinceName": "天津"
                    }
                ]
            }
        ],
        "RequestId": "b6b42d29-1ec7-437a-a396-826f44ae344e"
    }
}
```