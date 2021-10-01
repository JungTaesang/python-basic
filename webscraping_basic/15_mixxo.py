import csv
import requests
from bs4 import BeautifulSoup
goods_ids = []
count = 0
TARGET_CTGRS = ["1902380396","1802341066","1802341060","1607300303","1607300297","1607300300","2011481031"]
tag_dict = {"1902380396":"OUTER", 
            "1802341066":"TOP", 
            "1802341060":"BOTTOM",
            "1607300303":"DRESS",
            "1607300297":"BAGS",
            "1607300300":"SHOES",
            "2011481031":"MUFFLER"
            }
COMMON_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
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
    'list_only_yn': '',
}
for ctgr_no in TARGET_CTGRS:
    initial_data['disp_ctg_no'] = ctgr_no
    initial_data['category_2depth'] = ctgr_no
    tag = tag_dict[ctgr_no]

    url = "https://m-mixxo.elandmall.com/dispctg/initDispCtg.action"
    res = requests.post(url, headers=COMMON_H, data=initial_data)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    print(soup)
    ls = soup.select("li")
    #print(ls)

    for l in ls:
        _id = l.attrs.get("id")
        if _id is None:
            continue
        elif "goods" not in _id:
            continue
        elif str(goods_ids) in _id:
            continue
        else:
            goods_ids.append(_id.split("_")[-1])
            id = goods_ids[count]
            count += 1
        url = "https://m-mixxo.elandmall.com/goods/initGoodsDetailLayer.action?goods_no=" + id
        print("\n" + url)
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"})
        soup2 = BeautifulSoup(res.text, 'html.parser')
        name = soup2.find("h3", attrs={"class":"gd_name"}).get_text()
        price = soup2.select_one(".prc > .sp").text
        print(f"종류 : {tag} \n이름 : {name}\n가격 : {price}")