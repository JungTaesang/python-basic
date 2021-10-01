import csv
import requests
from bs4 import BeautifulSoup
TARGET_CTGRS = ['1607300303']
COMMON_H = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
initial_data = {
    'kwd': '',
    'disp_ctg_no': '1902380396',
    'category_1depth': '',
    'category_2depth': '1902380396',
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

    url = "https://m-mixxo.elandmall.com/dispctg/initDispCtg.action"
    res = requests.post(url, headers=, data=initial_data)
    soup = BeautifulSoup(res.text, 'html.parser')
ls = soup.select("li")
goods_ids = []
for l in ls:
    _id = l.attrs.get("id")
    if _id is None:
        continue
    elif "goods" not in _id:
        continue
    goods_ids.append(_id.split("_")[-1])
    print(_id)
#res = requests.get("https://m-mixxo.elandmall.com/goods/initGoodsDetailLayer.action?goods_no=2106061737", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"})
#soup2 = BeautifulSoup(res.text, 'html.parser')
#응나가격 = soup2.select_one(".prc > .sp").text
# print(응나가격)
