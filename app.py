from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(host="localhost", user="fish_manager", password="admin", database="iot_data", charset="utf8mb4")


@app.route('/')
def index():
    count = int(request.args.get('count', 10))  # 溫度資料筆數
    turb_count = int(request.args.get('turb_count', 10))  # 濁度資料筆數
    feed_count = int(request.args.get('feed_count', 10))  # 餵食紀錄筆數

    conn = get_connection()
    cursor = conn.cursor()

    # 最新 1 筆感測資料
    cursor.execute("SELECT * FROM sensor_data ORDER BY datetime DESC LIMIT 1")
    latest_sensor = cursor.fetchone()

    # 餵食紀錄
    cursor.execute("SELECT * FROM feeding_log ORDER BY feeding_time DESC LIMIT %s", (feed_count,))
    feeding_logs = cursor.fetchall()

    # 趨勢圖用的水溫資料
    cursor.execute("SELECT datetime, temperature, turbidity_ntu FROM sensor_data ORDER BY datetime DESC LIMIT %s", (count,))
    chart_data = cursor.fetchall()

    # 趨勢圖用的濁度資料
    cursor.execute("SELECT datetime, turbidity_ntu FROM sensor_data ORDER BY datetime DESC LIMIT %s", (turb_count,))
    turb_chart_data = cursor.fetchall()

    conn.close()

    times = [row[0].strftime('%Y-%m-%d %H:%M') for row in reversed(chart_data)]
    temps = [row[1] for row in reversed(chart_data)]
    turbs = [row[2] for row in reversed(chart_data)]

    turb_times = [row[0].strftime('%Y-%m-%d %H:%M') for row in reversed(turb_chart_data)]
    turb_values = [row[1] for row in reversed(turb_chart_data)]

    return render_template("index.html", 
                           sensor=latest_sensor, 
                           logs=feeding_logs, 
                           times=times, temps=temps, turbs=turbs, count=count,
                           turb_times=turb_times, turb_values=turb_values, turb_count=turb_count,
                           feed_count=feed_count)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
