# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Field, Item


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id =Field()
    name = Field()
    url_token = Field()
    avatar_url = Field()
    avatar_url_template = Field()
    is_org = Field()
    type = Field()
    url = Field()
    user_type = Field()
    headline = Field()
    gender = Field()
    is_advertiser = Field()

    is_vip = Field()
    rename_days = Field()
    badge = Field()
    allow_message = Field()
    is_following = Field()
    is_followed = Field()
    follower_count = Field()
    answer_count = Field()
    articles_count = Field()
    employments = Field()

'''
id	2929c0c75d8d742cc9333b507145bf39
url_token	chen-feng-bao-lie-jiu-30-67
name	陈风暴烈酒
avatar_url	https://pic2.zhimg.com/v2-890d90b9befe949f40aa7636a4090d05_is.jpg
avatar_url_template	https://pic2.zhimg.com/v2-890d90b9befe949f40aa7636a4090d05_{size}.jpg
is_org	false
type	people
url	https://www.zhihu.com/people/chen-feng-bao-lie-jiu-30-67
user_type	people
headline	齐藤朱夏、南条爱乃、希魔王、小宫有纱、逢田姐、南小鸟哪个不是我老婆！？！
gender	1
is_advertiser	false
vip_info	{…}
is_vip	false
rename_days	60
badge	[]
allow_message	true
is_following	false
is_followed	false
is_blocking	false
follower_count	26916
answer_count	4415
articles_count	33
employments	[]
'''
