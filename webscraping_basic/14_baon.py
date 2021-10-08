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

filename = "바온_1.csv"
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

tag_dict= {39: "MADE",
           33: "OUTER",
           34: "TOP",
           178: "PANTS",
           177: "SKIRT",
           36: "DRESS",
           37: "ACC",
           54: "UNISEX",
           122: "BOY"}

invalid_ctgrs = ["56", "207","132","85","38","75","57"]
invalid_page = ["207","85","132","38"]
# 카테고리 페이지 내에서 페이지네이션 
for ctgr_no in ctgrs_no:
    ctgr_url = get_url(ctgr_no, 1)

    if str(ctgr_no) in invalid_ctgrs: continue
    tag = tag_dict[ctgr_no]
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

        print("\n" + page_url)
        if str(ctgr_no) in invalid_page:
            items =  soup.find_all("ul", {"class": "prdList"})[0].find_all("div", attrs = {"class":"thumbnail"})
        else:
            items =  soup.find_all("ul", {"class": "prdList"})[1].find_all("div", attrs = {"class":"thumbnail"})

        for items in items:
            item_link = "https://ba-on.com" + items.find("a")["href"]
            soup = get_soup(item_link)
            item = soup.find_all("tr", attrs={"class":"xans-record-"})[0].find("td")

            for item in item:
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
                    print(f"\n제품 이름 : {name} \n소비자 가격 : {Price_1} \n판매 가격 : {Price_2} \n제품 링크 {item_link}")
                elif "할인판매가" in sale:
                    Price = "(할인)" + soup.find_all("tr",attrs = {"class":"xans-record-"})[2].find("td").get_text()
                    print(f"\n제품 이름 : {name} \n제품 가격 : {Price} \n제품 링크 {item_link}")
                    date = [tag, name, "", Price , item_link]
                    writer.writerow(date)
                else: 
                    Price = soup.find_all("tr",attrs = {"class":"xans-record-"})[1].find("td").get_text()
                    print(f"\n제품 이름 : {name} \n제품 가격 : {Price} \n제품 링크 {item_link}")
                    date = [tag, name, "", Price , item_link]
                    writer.writerow(date)