# encoding: utf-8
from time import sleep
import requests
import json
import xlwt
import re
import yaml
import os
import sys

with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'config.yaml'), encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
print(data)
user_query = data['user_query']
file_name = data['file_name']
headers = {
    "x-csrf-token": "x",
}

offset = 1
store_list = []
while True:
    data = {"cacheKey":"JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkphcGFuJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyQ2hJSjk0RXJBMEh0R0dBUkwtR0ZpNFozeFVVJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmdvb2dsZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTM1Ljc0MDg1MzMlMkMlMjJsb25naXR1ZGUlMjIlM0ExMzkuNjc3MSU3RA==/DELIVERY/小竹向原//0/0//JTVCJTVE//////ALL/SEARCH_SUGGESTION/HOME//","feedSessionCount":{"announcementCount":0,"announcementLabel":""},"userQuery":user_query,"date":"","startTime":0,"endTime":0,"carouselId":"","sortAndFilters":[],"marketingFeedType":"","billboardUuid":"","feedProvider":"","promotionUuid":"","targetingStoreTag":"","venueUuid":"","favorites":"","vertical":"ALL","searchSource":"SEARCH_SUGGESTION","pageInfo":{"offset":offset,"pageSize":80}}
    r = requests.post("https://www.ubereats.com/api/getFeedV1?localeCode=jp-JP", json=data, headers=headers).json()
    data = r['data']['feedItems']
    hasmore = r['data']['meta']['hasMore']
    for v in data:
        store_list.append(v['uuid'])
    if hasmore != True:
        break
    offset += 80
    sleep(0.1)
print(len(store_list))
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('1',cell_overwrite_ok=True)
col = ('#','邮政编码','食品分类','店名','地址','评价数量','评价星数','钱的标志','营业时间')
for i in range(9):
    worksheet.write(0,i,col[i])
i = 1
for id in  store_list:
    data_store={"storeUuid":id}
    r = requests.post(
        "https://www.ubereats.com/api/getStoreV1", json=data_store, headers=headers).json()
    worksheet.write(i,0,i)

    
    try:
        worksheet.write(i,3,r['data']['title'])
    except:
        worksheet.write(i,3,'null')
    try:
        worksheet.write(i,1,r['data']['location']['postalCode'])
        worksheet.write(i,4,r['data']['location']['address'])
    except:
        worksheet.write(i,1,'null')
        worksheet.write(i,4,'null')
    
    try:
        worksheet.write(i,5,r['data']['rating']['reviewCount'])
        worksheet.write(i,6,r['data']['rating']['ratingValue'])
    except:
        worksheet.write(i,5,"null")
        worksheet.write(i,6,"null")
    try:
        if re.match(r'¥+',list(r['data']['categories'])[0],re.M|re.I):
            worksheet.write(i,2,list(r['data']['categories'])[1:])
            worksheet.write(i,7,list(r['data']['categories'])[0])
        else:
            worksheet.write(i,2,list(r['data']['categories']))
            worksheet.write(i,7,'null')  
    except:    
        worksheet.write(i,2,'null')
        worksheet.write(i,7,'null')   
    
    try:
        for t in r['data']['hours'][0]['sectionHours']:
            t['endTime'] /= 60
            t['startTime'] /= 60
        worksheet.write(i,8,str(list(r['data']['hours'][0]['sectionHours'])))
    except:
        worksheet.write(i,8,'null')
    
    i += 1
    sleep(0.1)
    print(r['data']['title'])

workbook.save(file_name)