import csv
import urllib.request
import requests
import re
from datetime import datetime, time
from bs4 import BeautifulSoup
from requests import Session

#filename = "컬리.csv"
#f = open(filename, "w", encoding="utf-8-sig", newline="")
#writer = csv.writer(f)
#title = ["제품이름", "판매가격", "회원할인가", "판매단위", "중량/용량","제품링크"]
#writer.writerow(title)

filename_2 = "컬리_리뷰.csv"
f_2 = open(filename_2, "w", encoding="utf-8-sig", newline="")
writer_2 = csv.writer(f_2) #quoting=csv.QUOTE_NONE ,escapechar=' ')
title_2 = ["제목", "날짜", "내용"]
writer_2.writerow(title_2)

#https://dojang.io/mod/page/view.php?id=2476
s = requests.Session()
class Crawler:
    def __init__(self) -> None:
        self.__jwtToken = None
        self.session = None
        self.init_session()

    # TODO: Getter Setter 공부
    # TODO: Private, Protect Variable 공부.
    @property
    def token(self):
        return self.__jwtToken
    
    @token.setter
    def token(self, jwt_token: str):
        #print("hhhh: ", jwt_token)
        self.__jwtToken = jwt_token

    def set_header(self):
        self.session.headers['authorization'] = 'Bearer ' + self.token

    def init_session(self):
        s = Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"
        self.session = s
        self.set_token_from_site()

    def set_token_from_site(self):
        day = datetime.today().strftime("%y%m%d")
        res = self.session.get(
            f"https://www.kurly.com/shop/event/kurlyEvent.php?htmid=event/join/join_{day}")
        txt = res.text
        area = txt[txt.find("var jwtToken"): txt.find("var apiDomain") - 2]
        self.token = re.sub("\'", '', area.split("=")[1]).strip()
        self.set_header()


def get_json(url):
    res = c.session.get(url)
    res.raise_for_status()
    return res.json()

#파이썬 인코딩 euc-kr

MAX_PAGE = 1000
goods_id = []
total = []
small_title = []
a = []
c = Crawler()
for page in range(1, MAX_PAGE):
    url = f"https://api.kurly.com/v2/home/search?keyword=cj&sort_type=-1&page_limit=21&page={page}&delivery_type=0&ver=1633846524215"
    j = get_json(url)
    total = j["paging"]["total"]
    if total == len(goods_id):
        break

    for item_id in j["data"]["products"]:
        get_id = item_id["no"]

        if get_id in goods_id:continue
        else: goods_id.append(get_id)
        url = f"https://api.kurly.com/v3/home/products/{get_id}"
        i = get_json(url)

        #image_url = i["data"]["detail_image_url"]
        #path = "C:/image/" + f"{get_id}.png"
        #urllib.request.urlretrieve(image_url, path)

        #name = i["data"]["name"]
        #price = i["data"]["original_price"]
        #unit_text = i["data"]["unit_text"]
        #weight = i["data"]["weight"]
        #discounted_price = i["data"]["discounted_price"]
        #if price == discounted_price: discounted_price = ""
        #link = f"https://www.kurly.com/shop/goods/goods_view.php?&goodsno={get_id}"
        #data = [name, price, discounted_price, unit_text, weight,link]
        #writer.writerow(data)
        #print(data)
        print(len(goods_id))

        #for page_idx in range(1,101):
        #    url = f"https://www.kurly.com/shop/goods/goods_review_list.php?goodsno={get_id}&page={page_idx}]"
        #    res = c.session.get(url)
        #    res.raise_for_status()
        #    soup = BeautifulSoup(res.content.decode('cp949', 'ignore'), "html.parser") 
#
        #    index = 0 
        #    day_list = []
#
        #    if page_idx == 1:
        #        day = soup.find_all("td", attrs={"class":"time"})[2:]
        #        review = soup.find_all("div", attrs={"class":"inner_review"})[2:]
        #        big_titles = soup.find_all("strong", attrs={"class":"name"})[2:]
        #        small_titles = soup.find_all("p", attrs={"class":"package"})[2:]
#
        #    else:
        #        day = soup.find_all("td", attrs={"class":"time"})
        #        review = soup.find_all("div", attrs={"class":"inner_review"})
        #        big_titles = soup.find_all("strong", attrs={"class":"name"})
        #        small_titles = soup.find_all("p", attrs={"class":"package"})
#
        #    for big_titles in big_titles:
        #        big_title = big_titles.get_text()
        #        if big_title not in a:
        #            a.append(big_title)
        #        
#
        #    for small_titles in small_titles:
        #        small_titles = small_titles.get_text()
        #        if small_titles not in small_title:
        #            small_title.append(small_titles)
#
        #    for day in day:
        #            day = day.get_text()
        #            day_list.append(day)
#
        #    for review in review:
        #        review = review.get_text()
        #        review = review.split('\n')
        #        review = list(set(review))
        #        review.remove('')
        #        review.remove(big_title)
        #        if small_title in review: review.remove(small_title)
        #        review = " ".join(review)
#
        #        if "\x00" in review:
        #            review = review.split('\x00')
        #            review = " ".join(review)
#
        #        data_2 = [big_title, day_list[index], review]
        #        print(data_2)
        #        writer_2.writerow(data_2)
        #        print(len(goods_id))
        #        index += 1