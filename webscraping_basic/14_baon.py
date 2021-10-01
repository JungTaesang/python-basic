import csv
import requests
from bs4 import BeautifulSoup

def get_url (ctgr_no, page_no): 
    return f"https://ba-on.com/product/list.html?cate_no={ctgr_no}&page={page_no}"

def get_soup (url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return BeautifulSoup(res.text, "lxml")    

filename = "바온_3.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

name = ["카테고리", "제품이름", "소비자가격", "판매가격", "제품링크"]
writer.writerow(name)

list_ = []
# 카테고리 목록 수집
main_soup = get_soup("https://ba-on.com/index.html")
ctgrs = main_soup.select_one(".Menu_list").select("li > a")
ctgrs_no= [int(c.attrs.get("href").split("cate_no=")[-1]) for c in ctgrs]
ctgrs_no.remove(39)
ctgrs_no.append(39)

# 카테고리 페이지 내에서 페이지네이션 
for ctgr_no in ctgrs_no:
    ctgr_url = get_url(ctgr_no, 1)
    if "https://ba-on.com/product/list.html?cate_no=56" in ctgr_url: continue
    elif "https://ba-on.com/product/list.html?cate_no=207" in ctgr_url: continue
    elif "https://ba-on.com/product/list.html?cate_no=132" in ctgr_url: continue
    elif "https://ba-on.com/product/list.html?cate_no=85" in ctgr_url: continue
    elif "https://ba-on.com/product/list.html?cate_no=38" in ctgr_url: continue
    elif "https://ba-on.com/product/list.html?cate_no=57" in ctgr_url: continue
    ctgr_soup = get_soup(ctgr_url)
    pages_area = ctgr_soup.select_one("div.ec-base-paginate-text")
    href = pages_area.find("a", {"class":"last"}).get("href")
    last_page = 1
    if href == "#none":
        pages = pages_area.find_all("li")
        if len(pages) == 1 and pages[0].a.text == '1':
            pass
    else:
        last_page = int(href.split("page=")[1])
    # 페이지 별 아이템 목록 수집
    for curr_page in range(1, last_page + 1):
        page_url = get_url(ctgr_no, curr_page)
        soup = get_soup(page_url)
        if "https://ba-on.com/product/list.html?cate_no=39" in page_url: tag = "MADE"
        elif "https://ba-on.com/product/list.html?cate_no=33" in page_url: tag = "OUTER"
        elif "https://ba-on.com/product/list.html?cate_no=34" in page_url: tag = "TOP"
        elif "https://ba-on.com/product/list.html?cate_no=178" in page_url: tag = "PANTS"
        elif "https://ba-on.com/product/list.html?cate_no=177" in page_url: tag = "SKIRT"
        elif "https://ba-on.com/product/list.html?cate_no=36" in page_url: tag = "DRESS"
        elif "https://ba-on.com/product/list.html?cate_no=37" in page_url: tag = "ACC"
        elif "https://ba-on.com/product/list.html?cate_no=54" in page_url: tag = "UNISEX"
        elif "https://ba-on.com/product/list.html?cate_no=122" in page_url: tag = "BOY"

        print("\n" + page_url)
        if "https://ba-on.com/product/list.html?cate_no=207" in page_url or "https://ba-on.com/product/list.html?cate_no=85" in page_url or "https://ba-on.com/product/list.html?cate_no=132" in page_url or "https://ba-on.com/product/list.html?cate_no=38" in page_url or "https://ba-on.com/product/list.html?cate_no=57" in page_url:
            items =  soup.find_all("ul", {"class": "prdList"})[0].find_all("div", attrs = {"class":"thumbnail"})
        else:
            items =  soup.find_all("ul", {"class": "prdList"})[1].find_all("div", attrs = {"class":"thumbnail"})


        for items2 in items:
            item_link = "https://ba-on.com" + items2.find("a")["href"]
            #print(item_link)
            soup = get_soup(item_link)
            item_ = soup.find_all("tr", attrs={"class":"xans-record-"})[0].find("td")
            #print(item_)

            for item in item_:
                item_id = item_link.split("/")[5]
                if item_id in list_: continue
                else: list_.append(item_id)
                name = item.get_text()
                Price_ = soup.find_all("tr", attrs={"class":"xans-record-"})[1].get_text()
                sale = soup.find_all("tr", attrs={"class":"xans-record-"})[2].get_text()

                if "소비자가" in Price_:
                    Price_1 = soup.find_all("tr", attrs={"class":"xans-record-"})[1].find("td").get_text()
                    Price_2 = soup.find_all("tr", attrs={"class":"xans-record-"})[2].find("td").get_text()
                    date = [tag, name, Price_1, Price_2 , item_link]
                    writer.writerow(date)
                    #print(f"\n제품 이름 : {title} \n소비자 가격 : {Price_1} \n판매 가격 : {Price_2} \n제품 링크 {item_link}")
                elif "할인판매가" in sale:
                    Price = "(할인)" + soup.find_all("tr",attrs = {"class":"xans-record-"})[2].find("td").get_text()
                    #print(f"\n제품 이름 : {title} \n제품 가격 : {Price} \n제품 링크 {item_link}")
                    date = [tag, name, "", Price , item_link]
                    writer.writerow(date)
                else: 
                    Price = soup.find_all("tr",attrs = {"class":"xans-record-"})[1].find("td").get_text()
                    #print(f"\n제품 이름 : {title} \n제품 가격 : {Price} \n제품 링크 {item_link}")
                    date = [tag, name, "", Price , item_link]
                    writer.writerow(date)