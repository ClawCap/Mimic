# 平台 API 参考

## 微博 (Weibo)

### 移动端 API（需cookie，通过 ManoBrowser fetch_api）

```bash
# 用户信息
GET https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=100505{uid}

# 用户微博列表（翻页）
GET https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}&page={page}

# 搜索用户
GET https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D{keyword}&page_type=searchall
```

**注意**：
- 直接 curl 返回 HTTP 432（需cookie）
- 必须通过 ManoBrowser `fetch_api` 带 cookie 请求
- 每页约 10 条微博

---

## B站 (Bilibili)

### 视频信息（不需要cookie）

```bash
# 视频详情（获取 aid/cid）
GET https://api.bilibili.com/x/web-interface/view?bvid={BV号}
# 返回: data.aid, data.cid, data.title

# 搜索视频
GET https://api.bilibili.com/x/web-interface/search/type?keyword={关键词}&search_type=video&order=click&page=1
# duration参数: 1(0-10min), 2(10-30min), 3(30-60min), 4(>60min)
```

### 字幕提取（需cookie）

```bash
# 获取字幕URL（通过 ManoBrowser fetch_api）
GET https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}
# 返回: data.subtitle.subtitles[0].subtitle_url

# 下载字幕JSON（直接curl，不需cookie）
GET https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/...
# 返回: { "body": [{ "from": 秒, "to": 秒, "content": "文字" }, ...] }
```

**注意**：
- 空间视频列表API（`/x/space/wbi/arc/search`）需 wbi 签名，不推荐
- 用搜索API替代空间API
- `fetch_api` 返回的是 OSS 链接，需二次 curl 下载

---

## 抖音 (Douyin)

### 视频播放URL（通过 ManoBrowser 浏览器操作）

```javascript
// 打开视频页
chrome_navigate("https://www.douyin.com/video/{video_id}")

// 等待5秒加载后，获取视频播放直链
chrome_execute_script(tabId, "MAIN",
    "() => { const v = document.querySelector('video'); return v ? (v.currentSrc || v.src || '') : ''; }")
```

```bash
# 下载视频（必须带 Referer）
curl -sL "{video_url}" -o video.mp4 \
  -H "Referer: https://www.douyin.com/" -H "User-Agent: Mozilla/5.0"
```

**注意**：
- 抖音无字幕API，必须用 Whisper 语音识别
- 播放URL有时效性（约2小时）
- 正片视频（>1小时）下载可能超时

---

## 百度百科

```bash
# 百科词条
GET https://baike.baidu.com/item/{词条名}
# 或带ID
GET https://baike.baidu.com/item/{词条名}/{ID}
```

**注意**：返回HTML，需 regex 提取文本。关键章节：早年经历、演艺经历、个人生活、人物评价。

**提取脚本**：
```bash
curl -sL "https://baike.baidu.com/item/{词条名}" -H "User-Agent: Mozilla/5.0" | \
  python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&[^;]+;', '', text)
text = re.sub(r'\s+', ' ', text).strip()
# 按章节搜索
for kw in ['早年经历', '演艺经历', '个人生活', '人物评价', '性格', '经典台词']:
    idx = text.find(kw)
    if idx >= 0:
        print(f'=== {kw} ===')
        print(text[idx:idx+400])
        print()
"
```

---

## 维基百科

```bash
GET https://zh.wikipedia.org/wiki/{词条名}
```

**注意**：中国大陆可能需要代理。提取方式同百度百科。

---

## 萌娘百科（动漫角色首选）

```bash
GET https://zh.moegirl.org.cn/{角色名}
```

**特点**：
- 动漫角色信息最全面（比百度百科详细数倍）
- 有"经典台词"/"名台词"专节
- 有"人际关系"/"角色关系"章节
- 有"性格"详细描述
- 可能有角色歌词、声优信息等

**注意**：萌娘百科偶尔有反爬，必要时通过 ManoBrowser 访问。

---

## Fandom Wiki（海外动漫/游戏）

```bash
GET https://{作品名}.fandom.com/zh/wiki/{角色名}
# 例: https://naruto.fandom.com/zh/wiki/漩涡鸣人
```

**特点**：
- 海外作品（火影、海贼、漫威等）的最全资料
- 有中文版（/zh/）但可能不完整，可切英文版
- 结构化程度高，方便提取

---

## 语录/名言网站

```bash
# 中文语录
搜索: site:mingyannet.com "{人名}"
搜索: "{人名}" 名言 经典语录

# 英文语录
GET https://www.goodreads.com/quotes/search?q={name}
GET https://www.brainyquote.com/authors/{name-slug}
```

**注意**：语录网站质量参差不齐，优先选有出处标注的。
