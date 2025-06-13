import time
import pymysql
import requests

# === 設定區 ===
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "iot_data",
    "charset": "utf8mb4"
}
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1378465773479006279/UElB-uyYo2Lat73ohQw3vRhEXRR1ZL_SNGmgSQngoIMKVlzt8FQS0sZOFKLILjO_0l4p"
CHECK_INTERVAL = 10  # 每幾秒檢查一次

# === 初始化上次通知 ID ===
last_sensor_id = None
last_feeding_id = None

def get_latest_row(cursor, table, id_col):
    cursor.execute(f"SELECT * FROM {table} ORDER BY {id_col} DESC LIMIT 1")
    return cursor.fetchone()

def send_discord_message(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

# === 監控迴圈 ===
while True:
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 檢查 sensor_data 表
        sensor_row = get_latest_row(cursor, "sensor_data", "id")
        if sensor_row and sensor_row[0] != last_sensor_id:
            last_sensor_id = sensor_row[0]
            _, datetime_val, temperature, turbidity_ntu = sensor_row

            # 發送正常更新訊息
            msg = f"🌡️ 感測數據更新：\n時間：{datetime_val}\n溫度：{temperature}°C\n濁度：{turbidity_ntu} NTU"
            send_discord_message(msg)

            # 發送警告訊息
            if turbidity_ntu > 50:
                alert_msg = f"🚨 警告：濁度過高！\n濁度：{turbidity_ntu} NTU（>50）\n時間：{datetime_val}"
                send_discord_message(alert_msg)
            if temperature < 20 or temperature > 30:
                alert_msg = f"🔥 警告：溫度異常！\n溫度：{temperature}°C（應在 20~35°C 間）\n時間：{datetime_val}"
                send_discord_message(alert_msg)

        # 檢查 feeding_log 表
        feeding_row = get_latest_row(cursor, "feeding_log", "id")
        if feeding_row and feeding_row[0] != last_feeding_id:
            last_feeding_id = feeding_row[0]
            _, feeding_time, temperature, turbidity_ntu = feeding_row

            # 發送正常更新訊息
            msg = f"🐟 餵食紀錄新增：\n時間：{feeding_time}\n溫度：{temperature}°C\n濁度：{turbidity_ntu} NTU"
            send_discord_message(msg)

        conn.close()
    except Exception as e:
        print(f"發生錯誤：{e}")

    time.sleep(CHECK_INTERVAL)


