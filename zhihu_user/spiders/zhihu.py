# -*- coding: utf-8 -*-
import scrapy
import re
import json
import scrapy
from zhihu_user.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
    }
    start_user = "excited-vczh"


    #这里把查询的参数单独存储为user_query,user_url存储的为查询用户信息的url地址
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"

    #follows_url存储的为关注列表的url地址,fllows_query存储的为查询参数。这里涉及到offset和limit是关于翻页的参数，0，20表示第一页
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&limit={limit}&offset={offset}"
    follows_query = "data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics"

    #followers_url是获取粉丝列表信息的url地址，followers_query存储的为查询参数。
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&limit={limit}&offset={offset}"
    followers_query = "data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics"


    def parse(self, response):
        pass





    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]


#知乎登录
    def login(self, response):
        response_text = response.text

        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))
        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "13265904500",
                "password": "oldbigcode520",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
                                 callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self,response):
        text_json = json.loads(response.text)
        print(text_json)

        if "msg" in text_json and text_json["msg"] == "登录成功":
            yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
            yield scrapy.Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
                                 headers=self.headers, callback=self.parse_follows)
            yield scrapy.Request(
                self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), headers=self.headers,
                callback=self.parse_followers)

    def parse_user(self, response):
        '''
        因为返回的是json格式的数据，所以这里直接通过json.loads获取结果
        :param response:
        :return:
        '''
        result = json.loads(response.text)
        item = UserItem()
        # 这里循环判断获取的字段是否在自己定义的字段中，然后进行赋值
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        # 这里在返回item的同时返回Request请求，继续递归拿关注用户信息的用户获取他们的关注列表
        print(item)
        yield item
        yield scrapy.Request(
            self.follows_url.format(user=result.get("url_token"), include=self.follows_query, offset=0, limit=20), headers=self.headers,
            callback=self.parse_follows)
        yield scrapy.Request(
            self.followers_url.format(user=result.get("url_token"), include=self.followers_query, offset=0, limit=20), headers=self.headers,
            callback=self.parse_followers)

    def parse_follows(self, response):
        '''
        用户关注列表的解析，这里返回的也是json数据 这里有两个字段data和page，其中page是分页信息
        :param response:
        :return:
        '''
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),headers=self.headers,
                              callback=self.parse_user)

        # 这里判断page是否存在并且判断page里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield scrapy.Request(next_page, headers=self.headers,callback=self.parse_follows)

    def parse_followers(self, response):
        '''
        这里其实和关乎列表的处理方法是一样的
        用户粉丝列表的解析，这里返回的也是json数据 这里有两个字段data和page，其中page是分页信息
        :param response:
        :return:
        '''
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),headers=self.headers,
                              callback=self.parse_user)

        # 这里判断page是否存在并且判断page里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield scrapy.Request(next_page,headers=self.headers, callback= self.parse_followers)