---
sidebar_position: 1
---

# روبوٹکس ایپلیکیشنز کے لیے انٹرایکٹو صفحات بنانا

کسٹم صفحات بنانا آپ کو روبوٹکس پروجیکٹس کے لیے انٹرایکٹو ڈیش بورڈز، ویژولائزیشن ٹولز، اور مانیٹرنگ انٹرفیسز بنانے کی اجازت دیتا ہے۔ یہ اسٹینڈالون صفحات ریئل ٹائم ڈیٹا، سمولیشن نتائج، اور کنٹرول انٹرفیسز کو یکجا کر سکتے ہیں۔

## روبوٹ اسٹیٹس ڈیش بورڈ بنانا

خصوصی انٹرفیسز بنانے کے لیے `src/pages` میں **React یا Markdown** فائلیں شامل کریں:

- `src/pages/index.js` → `localhost:3000/` (مین لینڈنگ پیج)
- `src/pages/control-panel.js` → `localhost:3000/control-panel` (روبوٹ کنٹرول انٹرفیس)
- `src/pages/simulation.js` → `localhost:3000/simulation` (سمیولیٹر ویژولائزیشن)
- `src/pages/telemetry.js` → `localhost:3000/telemetry` (ریئل ٹائم ڈیٹا ڈیش بورڈ)

## روبوٹ ٹیلی میٹری ڈیش بورڈ بنائیں

ریئل ٹائم روبوٹ ڈیٹا ویژولائز کرنے کے لیے `src/pages/robot-telemetry.js` پر فائل بنائیں:

```jsx title="src/pages/robot-telemetry.js"
import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';

// ماک ڈیٹا فیچنگ فنکشن - عملی طور پر، ROS2 ٹاپکس یا REST API سے جڑیں
const fetchTelemetryData = async () => {
  const mockData = {
    battery_level: 87,
    joint_positions: { hip: 0.2, knee: 1.1, ankle: -0.3 },
    imu_data: { roll: 0.01, pitch: 0.03, yaw: 1.57 },
    gps_location: { lat: 37.7749, lon: -122.4194 },
    cpu_temp: 65,
    status: 'ACTIVE'
  };
  return mockData;
};

export default function RobotTelemetryDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const telemetryData = await fetchTelemetryData();
      setData(telemetryData);
      setLoading(false);
    };

    loadData();
    // ہر 2 سیکنڈ میں ریفریش کریں
    const interval = setInterval(loadData, 2000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Layout title="روبوٹ ٹیلی میٹری">
        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <h1>ٹیلی میٹری ڈیٹا لوڈ ہو رہا ہے...</h1>
              <div className="progress">
                <div className="progress__bar progress__bar--animated"></div>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="روبوٹ ٹیلی میٹری ڈیش بورڈ">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col">
            <h1>روبوٹ ٹیلی میٹری ڈیش بورڈ</h1>
            <p>آخری اپ ڈیٹ: {new Date().toLocaleTimeString()}</p>
          </div>
        </div>

        <div className="row margin-vert--lg">
          {/* اسٹیٹس پینل */}
          <div className="col col--3">
            <div className={`card ${data.status === 'ACTIVE' ? 'card--success' : 'card--danger'}`}>
              <div className="card__header">
                <h3>سسٹم اسٹیٹس</h3>
              </div>
              <div className="card__body">
                <p>حیثیت: <strong>{data.status}</strong></p>
                <p>بیٹری: <strong>{data.battery_level}%</strong></p>
                <p>CPU درجہ حرارت: <strong>{data.cpu_temp}°C</strong></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
```

ایک نیا صفحہ اب [http://localhost:3000/robot-telemetry](http://localhost:3000/robot-telemetry) پر دستیاب ہے جو لائیو روبوٹ ڈیٹا دکھاتا ہے۔

## سمولیشن ویژولائزیشن پیج بنائیں

سمولیشن منظرنامے دکھانے کے لیے `src/pages/simulation-viewer.md` پر فائل بنائیں:

```mdx title="src/pages/simulation-viewer.md"
---
title: سمولیشن ماحول ویور
description: حقیقت پسندانہ ماحول میں روبوٹ سمولیشن ویژولائز کریں
---

# روبوٹ سمولیشن ماحول

یہ صفحہ مختلف ماحول میں ہمارے روبوٹ سمولیشن کے لیے انٹرایکٹو ویور فراہم کرتا ہے۔

## دستیاب منظرنامے

1. **گودام نیویگیشن**: پیکجز اٹھانے کے لیے گودام کی گلیوں میں نیویگیٹ کرنے والا روبوٹ
2. **شہری تلاش**: شہری ماحول میں تلاش اور ریسکیو کرنے والا روبوٹ
3. **صنعتی معائنہ**: صنعتی آلات اور ڈھانچوں کا معائنہ کرنے والا روبوٹ
4. **ہیومن-روبوٹ تعاون**: مینوفیکچرنگ کاموں میں انسانوں کی مدد کرنے والا روبوٹ

## خصوصیات

- ریئل ٹائم فزکس سمولیشن
- متحرک ماحولیاتی اشیاء
- سینسر سمولیشن (LiDAR، کیمرے، IMU)
- ٹکراؤ کا پتہ لگانا اور بچاؤ
- کارکردگی میٹرکس ٹریکنگ
```

کسٹم صفحات آپ کو روایتی دستاویزات سے آگے اپنی روبوٹکس ایپلیکیشنز کو کنٹرول، مانیٹر، اور ویژولائز کرنے کے لیے بھرپور، انٹرایکٹو انٹرفیسز بنانے کی اہلیت دیتے ہیں۔
