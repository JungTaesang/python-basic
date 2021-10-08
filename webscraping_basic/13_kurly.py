import csv
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from requests import Session
from requests.sessions import session

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
        print("hhhh: ", jwt_token)
        self.__jwtToken = jwt_token

    def set_header(self):
        self.session.headers['authorization'] = 'Bearer ' + self.token

    def init_session(self):
        s = Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"
        self.session = s

    def set_token_from_site(self):
        day = datetime.today().strftime("%y%m%d")
        res = self.session.get(
            f"https://www.kurly.com/shop/event/kurlyEvent.php?htmid=event/join/join_{day}")
        txt = res.text
        area = txt[txt.find("var jwtToken"): txt.find("var apiDomain") - 2]
        self.token = re.sub("\'", '', area.split("=")[1]).strip()
        self.set_header()
    
    def lets_crawl(self):
        self.set_token_from_site()




url = "https://api.kurly.com/v2/home/search?keyword=cj&sort_type=-1&page_limit=21&page=1&delivery_type=0&ver=1633421773554"
c = Crawler()
#j = res.json()
#items = res.find_all("span",attrs={"class":"screen_out"})