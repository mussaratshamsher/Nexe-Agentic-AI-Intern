---
sidebar_position: 3
---

# ہارڈ ویئر اور سافٹ ویئر سیٹ اپ

یہ ضمیمہ فزیکل AI اور ہیومنائیڈ روبوٹکس پروجیکٹس کے لیے ڈیولپمنٹ ماحول سیٹ اپ کرنے کی جامع گائیڈ فراہم کرتا ہے۔

## سسٹم کی ضروریات

### کم از کم سسٹم کی وضاحتیں
- CPU: Intel i5 یا مساوی AMD پروسیسر (4 کورز، 2.5 GHz یا تیز)
- RAM: کم از کم 8 GB (16 GB تجویز کردہ)
- اسٹوریج: 50 GB خالی ڈسک اسپیس (SSD تجویز کردہ)
- گرافکس: ڈیپ لرننگ استعمال کرتے ہوئے CUDA سپورٹ والا GPU (NVIDIA GTX 1060 یا بہتر)
- OS: Ubuntu 20.04 LTS، Windows 10/11، یا macOS 10.15+

### تجویز کردہ ڈیولپمنٹ مشین
- CPU: Intel i7/i9 یا مساوی AMD Ryzen پروسیسر (6+ کورز)
- RAM: 32 GB یا زیادہ
- اسٹوریج: 500 GB+ SSD
- گرافکس: CUDA سپورٹ والا NVIDIA RTX سیریز GPU

## سافٹ ویئر انسٹالیشن گائیڈ

### روبوٹ آپریٹنگ سسٹم (ROS)

ROS روبوٹکس ڈیولپمنٹ کے لیے معیاری فریم ورک ہے اور ہارڈ ویئر ایبسٹریکشن، ڈیوائس ڈرائیورز، لائبریریاں، ویژولائزرز، میسج پاسنگ، پیکج مینجمنٹ، اور بہت کچھ فراہم کرتا ہے۔

#### ROS 2 Humble Hawksbill انسٹال کرنا

```bash
# ROS 2 apt ریپوزٹری شامل کریں
sudo apt update && sudo apt install curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# ROS 2 پیکجز انسٹال کریں
sudo apt update
sudo apt install ros-humble-desktop
```

### سمولیشن ماحول

#### Gazebo سمیولیٹر
```bash
sudo apt install gazebo11 libgazebo11-dev
```

#### PyBullet فزکس انجن
```bash
pip3 install pybullet
```

### ڈیولپمنٹ ٹولز

#### IDE سیٹ اپ
روبوٹکس ڈیولپمنٹ کے لیے مناسب IDE انسٹال کریں:

```bash
sudo snap install --classic code
```

VSCode میں، یہ ایکسٹینشنز انسٹال کریں:
- ROS
- C/C++ Extension Pack
- Python Extension Pack
- Pylance

#### Python ماحول
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip3 install --upgrade pip

# روبوٹکس کے لیے ضروری Python پیکجز انسٹال کریں
pip3 install numpy scipy matplotlib
pip3 install torch torchvision torchaudio
pip3 install opencv-python
pip3 install stable-baselines3[extra]
```

## ہارڈ ویئر اجزاء کی گائیڈ

### سادہ ہیومنائیڈ روبوٹ بنانے کے لیے ضروری اجزاء

#### ایکچویٹرز (سروو موٹرز)
- **ہائی ٹارک سروز**: مین جوائنٹس (ٹانگیں، بازو) کے لیے - Dynamixel AX-12A، RX-24F، یا MX-28 سیریز تجویز کردہ
- **مائیکرو سروز**: باریک حرکات (ہاتھ، سر) کے لیے - SG90 یا MG996R سروز

#### سینسرز
- **IMU (Inertial Measurement Unit)**: توازن اور رخ کے لیے MPU6050 یا BNO055
- **فورس/ٹارک سینسرز**: پاؤں کے رابطے کی شناخت اور مینی پولیشن کے لیے
- **کیمرہ ماڈیول**: ویژن کے لیے Raspberry Pi کیمرہ یا USB ویب کیم
- **فاصلے کے سینسرز**: الٹراسونک (HC-SR04) یا ٹائم آف فلائٹ سینسرز (VL53L0X)

#### پروسیسنگ یونٹس
- **سنگل بورڈ کمپیوٹر**: آن بورڈ پروسیسنگ کے لیے Raspberry Pi 4 (4GB+) یا NVIDIA Jetson Nano
- **مائیکرو کنٹرولر**: لو لیول ایکچویٹر کنٹرول کے لیے Arduino Uno/Nano

## عام مسائل کا حل

### ROS انسٹالیشن کے مسائل
- اگر آپ کو "rosdep update" ایررز ملیں، اپنا انٹرنیٹ کنکشن چیک کریں
- اجازت کے مسائل کے لیے، یقینی بنائیں کہ آپ انسٹالیشن کی ہدایات کو بالکل فالو کر رہے ہیں

### ہارڈ ویئر مواصلات کے مسائل
- تمام کنکشنز اور پاور سپلائی لیولز چیک کریں
- مائیکرو کنٹرولرز اور کمپیوٹرز کے درمیان باؤڈ ریٹس میچ ہونے کی تصدیق کریں
- تمام اجزاء کی مناسب گراؤنڈنگ یقینی بنائیں

اس سیٹ اپ گائیڈ کی پیروی کرکے، آپ کے پاس فزیکل AI اور ہیومنائیڈ روبوٹکس کے تصورات کی کھوج کے لیے ایک مکمل ڈیولپمنٹ ماحول تیار ہونا چاہیے۔
