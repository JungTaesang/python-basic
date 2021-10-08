import csv
import urllib.request
from typing import Any, List
import requests
from bs4 import BeautifulSoup
filename = "미쏘.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
name = ["종류", "이름", "가격", "할인", "링크"]
writer.writerow(name)

TARGET_CTGRS = ["1902380396", "1802341066", "1802341060","1607300303", "1607300297", "1607300300", "2011481031"]
COMMON_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
AJAX_URL = "https://m-mixxo.elandmall.com/dispctg/initDispCtg.action"
MAX_PAGE = 1000
tag_dict = {"1902380396": "OUTER",
            "1802341066": "TOP",
            "1802341060": "BOTTOM",
            "1607300303": "DRESS",
            "1607300297": "BAGS",
            "1607300300": "SHOES",
            "2011481031": "MUFFLER"
            }
initial_data = {
    'kwd': '',
    'disp_ctg_no': '',
    'category_1depth': '',
    'category_2depth': '',
    'category_3depth': '',
    'category_4depth': '',
    'brand_no': '',
    'brand_nm': '',
    'vend_no': '',
    'vend_nm': '',
    'welfareYn': 'null',
    'staffDCYn': 'null',
    'min_price': '',
    'max_price': '',
    'min_rate': '',
    'max_rate': '',
    'color_info': '',
    'page_idx': 1,
    'pageSize': 60,
    'srchFd': 'null',
    'sort': 2,
    'listType': 'image',
    'applyStartDate': 'null',
    'applyEndDate': 'null',
    'dispStartDate': 'null',
    'dispEndDate': 'null',
    'newGoodsStartDate': 'null',
    'newGoodsEndDate': 'null',
    'mall_no': '0000043',
    'vend_info': '',
    'size_info': '',
    'deliCostFreeYn': '',
    'filter_info': '',
    'quick_deli_poss_yn': '',
    'lot_deli_yn': '',
    'field_recev_poss_yn': '',
    'normal_deli_yn': '',
    'fresh_deli_yn': '',
    'list_only_yn': 'Y',
}
def get_soup():
    res = requests.post(AJAX_URL, headers=COMMON_H, data=initial_data)
    return BeautifulSoup(res.text, 'html.parser')

def get_items(soup):
    goods_area = soup.select_one("#goods_list")
    if goods_area is not None and goods_area.ul is not None:
        return [g.attrs.get("id").split("_")[-1] for g in goods_area.ul.select("li")]
    return []

goods_ids = []
items = [] 
for ctgr_no in TARGET_CTGRS:
    initial_data['disp_ctg_no'] = ctgr_no
    initial_data['category_2depth'] = ctgr_no
    tag = tag_dict[ctgr_no]
    for page in range(1, MAX_PAGE):
        initial_data['page_idx'] = page
        soup = get_soup()
        page_goods_ids: List[Any] = get_items(soup=soup)
        if len(page_goods_ids) < 1:
            break

        goods_ids = page_goods_ids
        
        for item in goods_ids:
            url = "https://m-mixxo.elandmall.com/goods/initGoodsDetailLayer.action?goods_no=" + item
            if item in items:continue
            else: items.append(item)

            res = requests.post(url, headers=COMMON_H, data=initial_data)
            soup2 = BeautifulSoup(res.text, 'html.parser')

            name = soup2.find("h3", attrs={"class": "gd_name"}).get_text()
            price = soup2.select_one(".prc > .sp").text
            sale = soup2.find("dd" , attrs= {"class":"prc"}).get_text()
            if "%" in sale:
                sale = soup2.find("span" , attrs= {"class":"rt"}).get_text()
                print(f"\n페이지 : {page} \n종류 : {tag} \n이름 : {name} \n가격 : {price} \n할인 : {sale} \n링크 : {url}") 
                data = [tag, name, price, sale, url]
                writer.writerow(data)
            else:
                print(f"\n페이지 : {page} \n종류 : {tag} \n이름 : {name} \n가격 : {price} \n링크 : {url}")
                data = [tag, name, price, "", url]
                writer.writerow(data)

            #image_url = "https:" + soup2.find("div", attrs= {"class":"g_img"}).find("img")["src"]
            #path = "C:/image/" + f"{item}.png"
            #urllib.request.urlretrieve(image_url, path)
            #wget --no-check-certificate https://www.elandrs.com/upload/prd/img/538/600/2109659538_0000006.jpg