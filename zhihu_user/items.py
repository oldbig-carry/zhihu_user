# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    account_status = scrapy.Field()
    allow_message= scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    avatar_hue = scrapy.Field()
    avatar_url = scrapy.Field()
    avatar_url_template = scrapy.Field()
    badge = scrapy.Field()
    business = scrapy.Field()
    employments = scrapy.Field()
    columns_count = scrapy.Field()
    commercial_question_count = scrapy.Field()
    cover_url = scrapy.Field()
    description = scrapy.Field()
    educations = scrapy.Field()
    favorite_count = scrapy.Field()
    favorited_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_columns_count = scrapy.Field()
    following_favlists_count = scrapy.Field()
    following_question_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    gender = scrapy.Field()
    headline = scrapy.Field()
    hosted_live_count = scrapy.Field()
    is_active = scrapy.Field()
    is_bind_sina = scrapy.Field()
    is_blocked = scrapy.Field()
    is_advertiser = scrapy.Field()
    is_blocking = scrapy.Field()
    is_followed = scrapy.Field()
    is_following = scrapy.Field()
    is_force_renamed = scrapy.Field()
    is_privacy_protected = scrapy.Field()
    locations = scrapy.Field()
    is_org = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    url_token = scrapy.Field()
    user_type = scrapy.Field()
    logs_count = scrapy.Field()
    marked_answers_count = scrapy.Field()
    marked_answers_text = scrapy.Field()
    message_thread_token = scrapy.Field()
    mutual_followees_count = scrapy.Field()
    participated_live_count = scrapy.Field()
    pins_count =scrapy. Field()
    question_count =scrapy. Field()
    show_sina_weibo = scrapy.Field()
    thank_from_count = scrapy.Field()
    thank_to_count = scrapy.Field()
    thanked_count = scrapy.Field()
    type = scrapy.Field()
    vote_from_count = scrapy.Field()
    vote_to_count = scrapy.Field()
    voteup_count = scrapy.Field()