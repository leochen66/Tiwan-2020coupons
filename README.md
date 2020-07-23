# Tiwan-2020coupons

## 簡介
這是一個python的爬蟲程式，爬2020台灣四大振興卷(藝放卷、動茲卷、農遊卷、客家卷)的所有合作店家。

## 前置作業
```
pip install requests
pip install beautifulsoup4
```

## 測試
```
git clone https://github.com/leochen66/Tiwan-2020coupons
cd Tiwan-2020coupons
python demo.py
```

## 說明
Coupon.py實作了Class Coupon，包含四個method，分別為：get_farm(), get_efun(), get_don(), get_hakka()。 <br>
每個method實作一個網頁的爬蟲，執行後return一個json並寫成json檔儲存在data資料夾中，資料格式可以參考data資料夾中的檔案。