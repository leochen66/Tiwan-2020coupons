# Tiwan-2020coupons

## Introduction
This project is a Python crawler for Taiwan Promotion Coupons. In 2020, in order to support salers who suffered from economic decline that brought by COVID-19, the government laugh four kinds of coupons(culture, sports, farming and hakka-culture) to promote consumption. <br/> 
However, each sorts of coupons has different coperated stores(consumers are only able to use coupons in coperated stores). Ｔhis project collect stores data and store as json file.

這是一個python的爬蟲程式，爬2020台灣四大振興卷(藝放卷、動茲卷、農遊卷、客家卷)的所有合作店家。

## Requirement
```
pip install requests
pip install beautifulsoup4
pip install lxml
```

## How to Test ?
```
git clone https://github.com/leochen66/Tiwan-2020coupons
cd Tiwan-2020coupons
python demo.py
```

## Explanation
Class "Coupon" implemented in Coupon.py includes four methods: get_farm(), get_efun(), get_don(), get_hakka(). <br/> 
Each method return a json format data(collect from website) and write it to "data" folder. You can check the data format in this folder.

Coupon.py實作了Class Coupon，包含四個method，分別為：get_farm(), get_efun(), get_don(), get_hakka()。 <br>
每個method實作一個網頁的爬蟲，執行後return一個json並寫成json檔儲存在data資料夾中，資料格式可以參考data資料夾中的檔案。