import csv
import requests
import re
import datetime
from bs4 import BeautifulSoup


s = requests.Session()
s.headers

def set_token(self):
    day = datetime.today().strftime("%y%m%d")
    res = self.session.get(
        f"https://www.kurly.com/shop/event/kurlyEvent.php?htmid=event/join/join_{day}")
    txt = res.text
    area = txt[txt.find("var jwtToken"): txt.find("var apiDomain") - 2]
    self.__jwtToken = re.sub("\'", '', area.split("=")[1]).strip()

def set_header(self):
    self.session.headers['authorization'] = 'Bearer ' + self.tokens

url = "https://www.kurly.com/shop/goods/goods_search.php?searched=Y&log=1&skey=all&hid_pr_text=&hid_link_url=&edit=&sword=cj&x=6&y=18"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"}
#headers['authorization'] = 'Bearer ' + token

res = requests.get(url, headers = headers)
res.raise_for_status()

#items = res.find_all("span",attrs={"class":"screen_out"})

print(res.json())

#div class="group_btn" = 상품 아이디

#https://ba-on.com/product/unisex-%ED%94%84%ED%83%80-%EB%A1%B1-%EC%95%BC%EC%83%81-%EC%9E%90%EC%BC%93-2color/9580/category/40/display/1/