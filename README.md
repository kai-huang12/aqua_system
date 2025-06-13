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

資料庫結構
![image](https://github.com/user-attachments/assets/6a99f08a-5842-4ac6-8e66-950db6fc8a16)
![image](https://github.com/user-attachments/assets/fc279486-7c38-4b7c-b6bf-efacd04e2dc0)





