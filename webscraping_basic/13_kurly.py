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

url = "https://api.kurly.com/v2/home/search?keyword=cj&sort_type=-1&page_limit=21&page=1&delivery_type=0&ver=1633421773554"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"}
#headers['authorization'] = 'Bearer ' + token

res = requests.get(url, headers = headers)
res.raise_for_status()
j = res.json()
#items = res.find_all("span",attrs={"class":"screen_out"})

print(j)

#div class="group_btn" = 상품 아이디