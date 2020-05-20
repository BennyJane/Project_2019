#!/user/bin/env Python
#coding=utf-8

import requests
from lxml import etree

url="http://env.dhu.edu.cn/f9/4a/c8125a129354/page.htm"

header=headers ={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

res=requests.get(url,headers=header)
# res.encoding = "utf-8"
res=res.text

root=etree.HTML(res)
# print(res)

name=root.xpath("//div[@class='Article_Content']/p[1]/strong/span/text()")[0]
experieces=root.xpath("//div[@class='Article_Content']/p[2]/span[2]/text()")[0]
img=root.xpath("//div[@class='Article_Content']/p[2]/span[1]/span[1]/img/@src")[0]
all_img=url+img
print(name,'\n',all_img,'\n', experieces.strip("\n\r"),"\n",)

Third_part=root.xpath("//div[@class='Article_Content']/p[3]/span[1]/text()")
nums=len(Third_part)+1
for i in range(1,nums):
    try:
        Third_part=root.xpath("//div[@class='Article_Content']/p[3]/span[1]/text()[{}]".format(i))[0]
    except Exception as e:
            print(e)
    print(Third_part)



# Third_part=root.xpath("//div[@class='Article_Content']/p[3]/span[1]")[0]
# result=Third_part.xpath('string(.)').strip()
#
# print(len(Third_part),"\n",)

# for i in range(0,31):
#     item=root.xpath("//div[@class='Article_Content']/p[3]/span[1]")[0][i]
#     print(item)
#     print(str(etree.tostring(item), encoding='utf-8'))
    # print(bytes.decode(etree.tostring(item)))
# ustr=etree.tostring(Third_part)
# print(bytes.decode(etree.tostring(Third_part)))
