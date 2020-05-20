import requests
import json
import re
import math

url="https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=20&limit=20"
headers ={"User-Agent ":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"}

r=requests.get(url,headers=headers)
print(r.url)
print(r.content)

pattern = re.compile(r"&offset=(\d+)")
offset = pattern.search(url)
print(offset.group(1))
offset = offset.group(1)
print(type(offset))
next_offset = int(offset)+20
print(next_offset)
#print(url.sub( pattern,"&offset="+str(next_offset),1 ))

next_page = re.sub(r"&offset=(\d+)","&offset="+str(next_offset),url)
print(next_page)

