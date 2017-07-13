# -*- coding: utf-8 -*-

'''
爬天气后报历史数据http://www.tianqihoubao.com/lishi
'''

from bs4 import BeautifulSoup as bsp
import urllib,http.cookiejar,re,time


# 做好cookie管理工作
cookie=http.cookiejar.CookieJar() # 创建空CookieJar
cj=urllib.request.HTTPCookieProcessor(cookie) # 构造cookie
opener = urllib.request.build_opener(cj) # 根据cookie构造opener
# 伪造header
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'),
                     ('Connection',' keep-alive')]
# 载入header
urllib.request.install_opener(opener)

# 定义若干url
root_url='http://www.tianqihoubao.com/lishi/'

# 获取root_url网页内容
req = urllib.request.Request(root_url)
u=bsp(bytes.decode(urllib.request.urlopen(req).read(),'gbk'))

# 找到表格
u1=u.find(class_="citychk")

# 找到表格里的每一个市
u2=u1.find_all('dd')

# 记录每一个市的url和对应的中文名称
city_urls=[]
city_names=[]

for uu in u2:
    u3=uu.find_all('a')
    for u3u in u3:
        city_urls.append(re.split('\.|/',u3u.attrs['href'])[2])
        city_names.append(u3u.text)

months=['201201','201202','201203','201204','201205','201206','201207','201208','201209','201210','201211','201212','201301','201302','201303','201304','201305','201306','201307','201308','201309','201310','201311','201312','201401','201402','201403','201404','201405','201406','201407','201408','201409','201410','201411','201412','201501','201502','201503','201504','201505','201506','201507','201508','201509','201510','201511','201512','201601','201602','201603','201604','201605','201606','201607','201608','201609','201610','201611','201612']

# 构造各市历史月份url
for i,city_url in enumerate(city_urls):
    # 每爬一个市休息2秒钟
    time.sleep(2)
    with open('d:/weather/'+city_names[i]+'.csv','w') as f:
        f.write('日期,天气状况,气温,风力风向\n')
        for month in months:
            url_month='http://www.tianqihoubao.com/lishi/'+city_url+'/month/'+month+'.html'
            req = urllib.request.Request(url_month)
            
            #如果连接不成功，休息5分钟
            while True:
                try:
                    u=bsp(bytes.decode(urllib.request.urlopen(req).read(),'gbk'))
                    break
                except:
                    time.sleep(300)
                    
            # 删去不可见字符
            u1=[re.sub('\s','',x.text) for x in u.table.find_all('td')]
            
            # 写入文件的时候跳过表头
            for j,item in enumerate(u1[4:]):
                if j%4==3:
                    f.write(item+'\n')
                else:
                    f.write(item+',')