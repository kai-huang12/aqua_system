#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "RTClib.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP32Servo.h>

const char* ssid = "CHT1012";
const char* password = "0906600503";
const char* getFeedingURL = "http://192.168.0.102/get_last_feeding.php";
const char* insertFeedingURL = "http://192.168.0.102/insert_feeding.php";

#define ONE_WIRE_BUS 4
#define TURBIDITY_PIN 34
#define SERVO_PIN 15

RTC_DS3231 rtc;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);
Servo myServo;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi 已連線");

  if (!rtc.begin()) {
    Serial.println("無法偵測到 RTC");
    while (1);
  }

  tempSensor.begin();
  myServo.setPeriodHertz(50);
  myServo.attach(SERVO_PIN, 500, 2400);
  Serial.println("初始化完成");
}

String getLastFeedingTime() {
  HTTPClient http;
  http.begin(getFeedingURL);
  int code = http.GET();
  String payload = "";
  if (code > 0) {
    payload = http.getString();
  }
  http.end();
  return payload;
}

void sendSensorLog(String datetime, float temperature, float ntu) {
  HTTPClient http;
  http.begin("http://192.168.0.102/insert_sensor_data.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String postData = "datetime=" + datetime +
                    "&temperature=" + String(temperature) +
                    "&turbidity_ntu=" + String(ntu);

  int code = http.POST(postData);
  Serial.println("感測資料回應: " + http.getString());
  http.end();
}

void sendFeedingLog(String datetime, float temperature, float ntu) {
  HTTPClient http;
  http.begin(insertFeedingURL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String postData = "feeding_time=" + datetime +
                    "&temperature=" + String(temperature) +
                    "&turbidity_ntu=" + String(ntu);
  int code = http.POST(postData);
  Serial.println("伺服器回應: " + http.getString());
  http.end();
}

int timeDiffMinutes(DateTime now, String lastFeedStr) {
  if (lastFeedStr == "NONE") return 10000;

  int Y, M, D, h, m, s;
  // 用 sscanf 直接解析格式 "2025-05-31 19:50:00"
  if (sscanf(lastFeedStr.c_str(), "%d-%d-%d %d:%d:%d", &Y, &M, &D, &h, &m, &s) != 6) {
    Serial.println("⚠️ 餵食時間格式解析失敗");
    return 10000;
  }

  DateTime last(Y, M, D, h, m, s);
  TimeSpan diff = now - last;
  return diff.totalseconds() / 60;
}

void loop() {
  DateTime now = rtc.now();
  String datetime = now.timestamp(DateTime::TIMESTAMP_FULL);
  tempSensor.requestTemperatures();
  float temperature = tempSensor.getTempCByIndex(0);
  int raw = analogRead(TURBIDITY_PIN);
  float voltage = raw * (5.0 / 4095.0);
  float ntu = -1120.4 * sq(voltage) + 5742.3 * voltage - 4352.9;
  if (ntu < 0) ntu = 0;

  Serial.println("====================");
  Serial.println("時間: " + datetime);
  Serial.print("溫度: "); Serial.print(temperature); Serial.println(" °C");
  Serial.print("濁度(NTU): "); Serial.println(ntu);

  String lastFeedTime = getLastFeedingTime();
  int minutesSinceLastFeed = timeDiffMinutes(now, lastFeedTime);
  Serial.print("距離上次餵食: "); Serial.print(minutesSinceLastFeed); Serial.println(" 分鐘");

  if (temperature >= 20.0 && temperature <= 35.0 && ntu < 50.0 && minutesSinceLastFeed >= 1) {
    Serial.println("✅ 條件符合，執行餵食");
    myServo.write(90);
    delay(5000);
    myServo.write(0);
    sendFeedingLog(datetime, temperature, ntu);
  } else {
    Serial.println("❌ 不符合餵食條件");
  }

  sendSensorLog(datetime, temperature, ntu);

  delay(10000);
}
