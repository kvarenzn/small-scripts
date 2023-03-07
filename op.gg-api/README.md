# op.gg-api
抓包抓出来的op.gg网站的部分API

这里以jp.op.gg为例，其他区应该类似

经实际测试，无需api-key，只需伪造User-Agent。但有调用频次限制

## 基本概念
### `buildId`
一个长21字节的字符串，用于部分API调用（一般被用于URL中包含"`_next/data`"的API）。
暂未发现直接获取的方式。
在请求任意的jp.op.gg主/子网站时都会被包含在返回的html文件中。
一段简单获取`buildId`的Python示例代码如下

```python
import json
import requests
from bs4 import BeautifulSoup

def get_build_id() -> str:
	html = BeautifulSoup(requests.get('https://jp.op.gg', headers={
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
	}))  # 直接请求jp.op.gg，并解析返回的html数据
	next_data = json.loads(html.select_one('script#__NEXT_DATA__').contents[0])  # buildId在一个id为__NEXT_DATA__的script标签中，该标签保存了一个json对象
	return next_data['buildId']
```

### `summoner_id`

一个长46字节的字符串，每位玩家对应唯一的`summoner_id`。用于在绝大多数的玩家信息查询API中代指被查询的对象。

获取一位玩家对应的`summoner_id`的方法有很多，另外，一些API（如下边的“获取排行榜信息”API）在返回玩家昵称的同时会一并返回`summoner_id`。

## API列表

**注: 若无额外说明，则调用下方的API时均需要伪造User-Agent**

### 获取排行榜信息
#### URL
```
GET https://jp.op.gg/_next/data/{build_id}/leaderboards/{type}.json
```

#### 参数列表

##### URL参数

+ `build_id`
  + “基本概念”一节中介绍的buildId
+ `type`
  + 要获取的排行榜类型
  + 经测试，可选值为
    + `tier`: 默认排行榜
    + `champions`: 擅长英雄排行榜
    + `level`: 等级排行榜

##### 请求参数

+ `page`
  + 获取第`page`页的排行榜数据
  + 可选参数，默认为`1`
+ `region`
  + 排行榜所在的大区
  + 可选参数，参数为国家代号，例如日区为`jp`

### 根据昵称获取玩家信息

#### URL

```
GET https://jp.op.gg/_next/data/{build_id}/summoners/{region}/{name}.json
```

#### 参数列表

##### URL参数

+ `build_id`
  + “基本概念”一节中介绍的buildId
+ `region`
  + 要查询的大区代号，如日区为`jp`
+ `name`
  + 玩家昵称，使用UTF-8进行编码

##### 请求参数

+ `region`
  + 要查询的大区代号，如日区为`jp`
+ `summoner`
  + 玩家昵称，使用UTF-8进行编码

#### 示例

若需请求日区某位昵称为`example`的玩家信息，则请求URL为

(假设当日`build_id`为`000000000000000000000`)

```
GET https://jp.op.gg/_next/data/000000000000000000000/summoners/jp/example.json?region=jp&summoner=example
```

#### 备注

可以用来通过昵称获取`summoner_id`

### 根据`summoner_id`获取玩家信息

#### URL

```
GET https://jp.op.gg/api/summoners/{region}/{summoner_id}
```

#### 参数列表

##### URL参数

+ `region`
  + 要查询的大区代号，如日区为`jp`
+ `summoner_id`
  + 要查询的玩家的`summoner_id`

##### 请求参数

+ `hl`
  + 结果中文本使用的语言
  + 如简体中文为`zh_CN`
  + 可选
