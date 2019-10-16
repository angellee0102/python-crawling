#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.request as req
import bs4
import pandas as pd

url="https://tie.twtm.com.tw/WebPage/Technomart.aspx"
request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
root=bs4.BeautifulSoup(data,"html.parser")
titles=root.find_all("div",class_="stripeMeSLV margin5T margin10B")

# print(titles)
for title in titles:
    if title.a != None:
        # print(title.a.string)
        print(title.a.tt_id)

table=root.find_all('table',id="ContentPlaceHolder2_sgvTech")

print(len(table[0].find_all("tr")))

rawTable=table[0].find_all("tr")
for row in rawTable:
    # if row.td!=None:
        # 專利技術名稱
        # print(row.td.a.string)
    columns=row.find_all('td')
    for column in columns:
        print(column.get_text())


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')
driver = webdriver.Chrome("/Users/lee/Downloads/chromedriver", options=options)

driver.get(url)
table = driver.find_element_by_id('ContentPlaceHolder2_sgvTech')
# print('table',table)
# table_html = table.get_attribute('innerHTML')

# from pandas.io.html import read_html
# df = read_html(table_html)[0]
# print (df)
df=pd.DataFrame(columns=['專利技術名稱','流通方式','應用領域','功能'])


pages=55
list_data=[['專利技術名稱','流通方式','應用領域','功能']]
for page in range(2,pages-1):
#     print(page)
    driver.find_element_by_xpath('(//table[@id="ContentPlaceHolder2_sgvTech"]//tbody//tr)[last()]//td//a[contains(text(),"'+str(page)+'")]').click()
    time.sleep(3)
    tbody=driver.find_element_by_xpath('//table[@id="ContentPlaceHolder2_sgvTech"]//tbody')
    
    for row in tbody.find_elements_by_xpath(".//tr"):
        content=[td.text for td in row.find_elements_by_xpath(".//td")]
        print(content)
        list_data.append(content)
#         print(type([td.text for td in row.find_elements_by_xpath(".//td")]))
    df=pd.DataFrame(list_data,columns=['專利技術名稱','流通方式','應用領域','功能'])
#     print(df)
driver.close()

df=pd.DataFrame(list_data,columns=['專利技術名稱','流通方式','應用領域','功能'])


# In[ ]:


df


# In[ ]:


df.to_csv('參展技術.csv',index=False)


# In[ ]:


先進製造系統=df[df['應用領域'].str.contains("先進製造系統", na=False)]
先進製造系統.to_csv('先進製造系統.csv',index=False)


# In[ ]:


df1=pd.read_csv('參展技術.csv')
areas=['資訊與通訊','電子與光電','材料化工與奈米','生技與醫藥','先進製造系統','能源與環境','生活應用','農業相關']
for title in areas:
    table=df1[df1['應用領域'].str.contains(title, na=False)]
    table=table.drop(columns=[ '功能'])
    pathname=title+'.csv'
    table.to_csv(pathname,index=False)
    


# In[ ]:


熱塑高分子無機粉體分散相驗證及失效分析平台,非專屬授權,材料化工與奈米
含顆粒無菌包裝飲品製程研發技術與試量產服務平台,合作開發,生技與醫藥、生活應用
3D列印多孔金屬骨材,專屬授權、非專屬授權、合作開發,材料化工與奈米、生技與醫藥
微波複合能源烹調系統之最佳化設計與整合技術,非專屬授權,資訊與通訊、生技與醫藥
無人搬運載具,專屬授權、非專屬授權、合作開發,資訊與通訊、先進製造系統
深層海水微生物優化培育技術,合作開發,生技與醫藥、農業相關
小貝智能機器人／Bobby波比智能帶屏能音箱,專屬授權、合作開發、其他: (零售、代理),資訊與通訊、生活應用
『Chameleon』工業物聯網閘道與AI edge技術,其他: ,材料化工與奈米
低風阻彈壓織物技術,非專屬授權,材料化工與奈米
糖尿病視網膜病變診斷輔助分析系統,非專屬授權、合作開發,生技與醫藥


# In[ ]:




