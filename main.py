import requests
import urllib3
import re
import time
from bs4 import UnicodeDammit
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

with open('domain.txt','r') as f:
    domain_list=f.read().split('\n')

for doamin in domain_list:
    try:
        res = requests.get('http://'+doamin, headers=headers, verify=False, timeout=30)
        res.encoding = UnicodeDammit(res.content).original_encoding
        web_icp_list=re.findall('[京津沪渝冀晋辽吉黑苏浙皖蜀闽赣鲁豫鄂湘粤琼黔滇陕甘青台蒙桂藏宁新港澳]ICP备\d{8}号[-]?[\d*]{0,2}', res.text.replace('\n','').replace(' ',''))
        if web_icp_list != []:
            web_icp=web_icp_list[0]
        else:
            web_icp='无'
        visi = '是'
    except:
        try:
            res = requests.get('https://' + doamin, headers=headers, verify=False, timeout=30)
            res.encoding = UnicodeDammit(res.content).original_encoding
            web_icp_list = re.findall('[京津沪渝冀晋辽吉黑苏浙皖蜀闽赣鲁豫鄂湘粤琼黔滇陕甘青台蒙桂藏宁新港澳]ICP备\d{8}号[-]?[\d*]{0,2}', res.text.replace('\n','').replace(' ',''))
            if web_icp_list != []:
                web_icp = web_icp_list[0]
            else:
                web_icp = '无'
            visi = '是'
        except:
            visi='否'
            web_icp='/'
    try:
        res2=requests.get('https://api.muxiuge.com/api/beian/?domain=' + doamin, headers=headers, verify=False, timeout=30).json()
        if res2['success']==True:
            name=res2['result']['name']
            nature=res2['result']['nature']
            icp=res2['result']['icp']
        else:
            name = '无记录'
            nature = '无记录'
            icp = '无记录'
    except:
        name='查询失败'
        nature = '查询失败'
        icp = '查询失败'



    time.sleep(1)
    result = '{},{},{},{},{},{}\n'.format(doamin,web_icp, icp, name, nature, visi)
    print(result)
    with open('icp.txt','a') as f:
        f.write(result)



