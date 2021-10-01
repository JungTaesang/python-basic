import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

#네이버 웹툰 전체 목록 가져오기
cartoons = soup.find_all("a", attrs = {"class":"title"})
# a element 의 class 속성이 title 인 모든 element를 반환
for cartoon in cartoons:
    print(cartoon.get_text())
