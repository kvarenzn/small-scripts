## 说明
借助nginx的本地反代不支持SNI的特性，实现域名前置绕过GFW对某些网站的阻断（通常表现为CONNECTION RESET）
目前支持的网站列表如下（肯定不止这些）：
+ pixiv
+ wikipedia
+ github
    + githubassets
    + githubusercontent
    + gist
    + github.io
    + ssh&git访问 (通过stream重定向22和9418端口的请求)
+ steam
    + store
    + community
+ cloudflare-dns
+ picacomic
+ e-hentai / exhentai
+ onedrive
+ twitch
+ huggingface

## 使用
1. 自签CA证书，并设置系统信任该CA证书
2. 使用自签CA证书签名服务器证书，把被反代的域名都配置进去
3. 第二步得到的证书和key文件都放到`/usr/share/nginx/ca`下，分别重命名为`server.crt`和`server.key`
4. `nginx.conf`放到`/etc/nginx`下
5. 启动`nginx.service`
6. 配置hosts或本地dns服务器，让上述网站的网址指向本机`127.0.0.1`

## Hosts示例
一份hosts文件如下，仅供参考
```hosts
# pixiv
127.0.0.1 pixiv.net www.pixiv.net ssl.pixiv.net accounts.pixiv.net touch.pixiv.net public-api.pixiv.net oauth.secure.pixiv.net app-api.pixiv.net
127.0.0.1 i.pximg.net s.pximg.net
127.0.0.1 sketch.pixiv.net
127.0.0.1 factory.pixiv.net
127.0.0.1 dic.pixiv.net en-dic.pixiv.net sensei.pixiv.net fanbox.pixiv.net payment.pixiv.net
127.0.0.1 imgaz.pixiv.net comic.pixiv.net novel.pixiv.net source.pixiv.net i1.pixiv.net i2.pixiv.net i3.pixiv.net i4.pixiv.net

# wikipedia
127.0.0.1 www.wikipedia.org m.wikipedia.org en.wikipedia.org wikipedia.org en.m.wikipedia.org

# pica
127.0.0.1 picacomic.com www.picacomic.com picaapi.picacomic.com

# github
127.0.0.1 github.com www.github.com gist.github.com
127.0.0.1 raw.githubusercontent.com camo.githubusercontent.com
127.0.0.1 codeload.github.com

# cloudflare-dns
127.0.0.1 cloudflare-dns.com www.cloudflare-dns.com

# exhentai
127.0.0.1 exhentai.org www.exhentai.org forums.e-hentai.org

# steam
127.0.0.1 steamcommunity.com www.steamcommunity.com store.steampowered.com

# onedrive
127.0.0.1 onedrive.live.com

# twitch
127.0.0.1 www.twitch.tv twitch.tv gql.twitch.tv irc-ws.chat.twitch.tv pubsub-edge.twitch.tv

# huggingface
127.0.0.1 huggingface.co www.huggingface.co
```
