# aqua_system
簡易的智慧水產養殖系統，旨在幫助養殖業者以低成本的方式偵測水質
>使用光學濁度感測器模組偵測水質濁度，若濁度過高則暫停投餵飼料。
>使用溫度感測器偵測水溫，過高或高低的水溫皆可能導致魚群食慾不佳。
>使用時鐘模組紀錄餵食間隔，避免餵食頻率過高或高低。
>綜合以上功能，整合成水質偵測系統，並藉由機器判斷是否適合投餵飼料，同時自動投餵飼料，省去人工判斷及投餵飼料的時間，只需定期補充飼料庫存。

相關硬體需求：
1. SEN0189 光學濁度感測器模組
2. DS18b20 溫度感測器
3. SG90 伺服馬達
4. 高精度DS3231時鐘模組
5. Esp32 開發板

硬體連接圖

![image](https://github.com/user-attachments/assets/6550de4a-3cd5-490f-b82c-6c9847355d7b)

>開啟飼料投餵
<img width="338" height="300" alt="image" src="https://github.com/user-attachments/assets/23f424a8-5567-4930-9a65-c59449eaee5c" />

>關閉飼料投餵
<img width="333" height="298" alt="image" src="https://github.com/user-attachments/assets/e2711642-a609-4b7b-bd15-9c1b4b669504" />

資料庫結構

![image](https://github.com/user-attachments/assets/6a99f08a-5842-4ac6-8e66-950db6fc8a16)
![image](https://github.com/user-attachments/assets/fc279486-7c38-4b7c-b6bf-efacd04e2dc0)

Discord Webhook 通知

>Discord 及時水溫數值通知
<img width="408" height="298" alt="image" src="https://github.com/user-attachments/assets/655d88df-260b-4c11-895e-f51bdc92d082" />

>水質數據異常警示
<img width="416" height="298" alt="image" src="https://github.com/user-attachments/assets/d3e0463a-0fd8-442c-a68b-2499a2e7b3ee" />



#檔案須以github上方式擺放


檔案用途：
1. app.py：主控程式，連接MySQL，前端及後端處理
2. dc.py：藉由dc及時通知使用者警示及偵測訊息
3. index.html：前端網頁功能
4. style.css：前端網頁美化
5. iot.ino：硬體控制程式碼


網頁顯示結果：

![image](https://github.com/user-attachments/assets/68687269-7686-49f1-af1c-7cee6c7d8cf2)
![image](https://github.com/user-attachments/assets/45636ce9-2d2a-450a-9758-ab61a43efc7b)
![image](https://github.com/user-attachments/assets/286ac83e-ffbb-416a-b955-480e2bbadd75)










