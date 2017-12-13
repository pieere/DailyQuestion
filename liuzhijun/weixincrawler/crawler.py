# -*- coding: utf-8 -*-

import html
import json
import logging
import re
import time

import requests

import utils
from models import Post

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class WeiXinCrawler:
    def crawl_latest_10(self):
        """
        爬取最近10条数据
        :return:
        """

        url = "https://mp.weixin.qq.com/mp/profile_ext?" \
              "action=home&" \
              "__biz=MjM5MzgyODQxMQ==&" \
              "devicetype=android-24&" \
              "version=26051633&" \
              "lang=zh_CN&" \
              "nettype=WIFI&" \
              "a8scene=7&" \
              "pass_ticket=oZQqv0KR7zhxAix1SHUFLwI7p%2FiKH2NPWIdEmZidhitAOdpf873t%2BLEZU9Hnxx%2FT&" \
              "wx_header=1"

        headers = """
Host: mp.weixin.qq.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; 2014813 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN
x-wechat-uin: NTI1NDc3NTE4
x-wechat-key: c37a3f1c3525d70e6537599058680a1c1d38d754815c6f101c7bf3fbc5bbcd19f8c54895c965c0d624b36d11da34033eb5109c5e40524df3109f43943505a19d0b3f68bacb0b77cbae35a251a1722f98
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: rewardsn=1872e6d4042552713dff; wxtokenkey=990d7740963fdbea6cf44ba78c4166b7f9025262edc22a0977c781f8073b54aa; wxuin=525477518; devicetype=android-22; version=26051731; lang=zh_CN; pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK+YA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n; wap_sid2=CI7NyPoBElxldXVmX1B4VVVJbXdNTnh4SDZ2YXlMcURDWENucDhvWmZoMktqRmQzYWJVRXV6b29TYmJWX2VscG4zekh2ZzVxWVhmcGpraDBLUEg3LTZZNmNXYXl2S1lEQUFBfjCQmMPRBTgMQJRO
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.23&TBSVC=43602&CO=BK&COVC=043632&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= 2014813 &RL=720*1280&OS=5.1.1&API=22
Q-GUID: 9d4417681f44eeb4410b613d13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b


    
        """
        headers = utils.str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)

        if '<title>验证</title>' in response.text:
            logger.error("无法正确获取内容，请重新获取请求参数和请求头")
            exit()

        rex = "msgList = '({.*?})'"
        pattern = re.compile(pattern=rex, flags=re.S)
        match = pattern.search(response.text)
        if match:
            msg_list = match.group(1)
            logger.info("抓取数据： %s" % msg_list)
            msg_list = html.unescape(html.unescape(msg_list))
            self.save(msg_list)
        else:
            logger.warning("没有找到匹配的数据")

    def crawl_more(self, offset=0):
        """
        爬取更多文章
        :return:
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext?" \
              "action=getmsg&" \
              "__biz=MjM5MzgyODQxMQ==&" \
              "f=json&" \
              "offset={offset}&" \
              "count=10&" \
              "is_ok=1&" \
              "scene=&" \
              "uin=777&" \
              "key=777&" \
              "pass_ticket=lDUqy%2FK9AFwZZVe8RDrxTER0kM1SAjDpAhfBgj2bW4QyP8V2lsi9gMbN%2FTJ0Nq7w&" \
              "wxtoken=&" \
              "appmsg_token=935_GxAo%2BiWnvCj80gcRR5iWbvAetsVErB5CLhSNJg~~&" \
              "x5=1&" \
              "f=json".format(offset=offset)  # appmsg_token 也是临时的

        headers = """
Host: mp.weixin.qq.com
Connection: keep-alive
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; 2014813 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN
Accept: */*
Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIwMTc4ODE0Mw==&devicetype=android-22&version=26051731&lang=zh_CN&nettype=WIFI&a8scene=7&session_us=gh_5138cebd4585&pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK%2BYA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n&wx_header=1
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: rewardsn=1872e6d4042552713dff; wxtokenkey=990d7740963fdbea6cf44ba78c4166b7f9025262edc22a0977c781f8073b54aa; wxuin=525477518; devicetype=android-22; version=26051731; lang=zh_CN; pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK+YA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n; wap_sid2=CI7NyPoBElxNWnRoazhJNk5CQkdYQ3NBRXZBNmVYbDVncS1yVkdsVjFQYUpCU3J6UGZ1WmxubC1wT3p4WkE4ZFY0dnRpaDdlZnJ1ank4dkdZbXpnNUd2V2hpbjNQS2NEQUFBfjCimMPRBTgMQJRO
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.23&TBSVC=43602&CO=BK&COVC=043632&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= 2014813 &RL=720*1280&OS=5.1.1&API=22
Q-GUID: 9d4417681f44eeb4410b613d13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b




        """
        headers = utils.str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
            self.save(msg_list)
            # 递归调用
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                # TODO 等待时间做成可配置
                time.sleep(2)
                self.crawl_more(next_offset)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新获取请求参数和请求头")
            exit()



    @staticmethod
    def save(msg_list):
        """
         msg_list 是字符串
        "{\"list\":[{\"comm_msg_info\":{\"id....
        还需要经过字符反转义后，再用json转换成字典
        """
        # TODO 处理多图文 multi_app_msg_item_list
        msg_list = msg_list.replace("&quot;", "\\\"").replace("\/", "/")
        data = json.loads(msg_list)
        posts = data.get("list")
        for item in posts:
            msg_info = item.get("app_msg_ext_info")
            if msg_info:
                keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
                sub_data = utils.sub_dict(item.get("app_msg_ext_info"), keys)
                post = Post(**sub_data)
                logger.info('save data %s ' % post.title)
                try:
                    post.save()
                except Exception as e:
                    logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(item.get("comm_msg_info")))



    def comments(self):
        url = "https://mp.weixin.qq.com/mp/appmsg_comment?" \
              "action=getcomment&" \
              "scene=0&" \
              "__biz=MjM5MzgyODQxMQ==&" \
              "appmsgid=2650367634&idx=1&" \
              "comment_id=4200886237&" \
              "offset=0&" \
              "limit=100&" \
              "uin=777&" \
              "key=777&" \
              "pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK%25252BYA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n&" \
              "wxtoken=772433544&" \
              "devicetype=android-22&" \
              "clientversion=26051731&" \
              "appmsg_token=935_y3k7aPYswY7Sxv5NfnJQ5P3s7pyh0cCESH2HBO6tiDh-AT2w546J0z2TWJSUNeRHZ5jZ4VP1ACqFq58R&x5=1&" \
              "f=json"


    def detail(self):
        url = "https://mp.weixin.qq.com/mp/getappmsgext?" \
              "__biz=MjM5MzgyODQxMQ==&" \
              "mid=2650367634&" \
              "sn=ec23c954f7adad842d706c2ec687a35e&" \
              "idx=1&" \
              "scene=0&" \
              "ct=1513035896&" \
              "abtest_cookie=AwABAAoADAANAAkAJIgeALuIHgDZiB4A4YgeAPyIHgANiR4A74keAPqJHgAJih4AAAA=&" \
              "devicetype=android-22&" \
              "version=/mmbizwap/zh_CN/htmledition/js/appmsg/index393966.js&" \
              "f=json&" \
              "r=0.621072335796014&" \
              "is_need_ad=1&" \
              "comment_id=4200886237&is_need_reward=1&both_ad=0&" \
              "reward_uin_count=24&msg_daily_idx=1&is_original=0&" \
              "uin=777&" \
              "key=777&" \
              "pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK%25252BYA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n&" \
              "wxtoken=772433544&" \
              "devicetype=android-22&" \
              "clientversion=26051731&" \
              "appmsg_token=935_y3k7aPYswY7Sxv5NfnJQ5P3s7pyh0cCESH2HBO6tiDh-AT2w546J0z2TWJSUNeRHZ5jZ4VP1ACqFq58R&x5=1&" \
              "f=json"
        body = "is_only_read=1&" \
               "req_id=1316UAeacYluLiqDM6ijGMez&" \
               "pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK%25252BYA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n&" \
               "is_temp_url=0"

        headers = """
Host: mp.weixin.qq.com
Connection: keep-alive
Content-Length: 143
Origin: https://mp.weixin.qq.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; 2014813 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
Referer: https://mp.weixin.qq.com/s?__biz=MjM5MzgyODQxMQ==&mid=2650367634&idx=1&sn=ec23c954f7adad842d706c2ec687a35e&chksm=be9cddc689eb54d07cd27f260f8ce7bf48d5702dc59a7f9b32725a7fd02d8b4a34f58382e4f5&scene=0&ascene=7&devicetype=android-22&version=26051731&nettype=WIFI&abtest_cookie=AwABAAoADAANAAkAJIgeALuIHgDZiB4A4YgeAPyIHgANiR4A74keAPqJHgAJih4AAAA%3D&lang=zh_CN&pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK%2BYA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n&wx_header=1
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: wxuin=525477518; devicetype=android-22; version=26051731; lang=zh_CN; pass_ticket=wxW7ApnFNe01tZe42nkIH5EExbK+YA45O1NzaLk7uLZBPks8RzUA4gzD6hxU9V5n; wap_sid2=CI7NyPoBElx0QXBfYlBHVDJpaEFiMHlZWWc5UVV5OExJdjl1UnpOU3RJTzFqTDA3T2dHTmZ0Mk5iZUtRT01zc1BYLUVtVnFXa1kwWk9PMjZQVUdsaGp2Y1JXd3I3S2NEQUFBfjCN1cPRBTgMQAk=; rewardsn=9d737ca75d9db0cb78f6; wxtokenkey=bd89c1f6d9cea0c564c7801f458c9cd7676d17f4ecb6f887c4e769c80975284e
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.23&TBSVC=43602&CO=BK&COVC=043632&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= 2014813 &RL=720*1280&OS=5.1.1&API=22
Q-GUID: 9d4417681f44eeb4410b613d13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b


        """
        headers = utils.str_to_dict(headers)
        # body = utils.str_to_dict(body, join_symbol="&", split_symbol="=")
        response = requests.post(url, headers=headers, data=body, verify=False)
        result = response.json()
        print(result)





if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.detail()
    # crawler.crawl_latest_10()
    # crawler.crawl_more()
