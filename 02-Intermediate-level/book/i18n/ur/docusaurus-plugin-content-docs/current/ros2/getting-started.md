---
sidebar_position: 1
---

# فزیکل AI اور ہیومنائیڈ روبوٹکس کے لیے ROS 2 کے ساتھ شروع کرنا

ROS 2 (روبوٹ آپریٹنگ سسٹم 2) ضروری مڈل ویئر فریم ورک ہے جو ہیومنائیڈ روبوٹس کے مختلف اجزاء کے درمیان مواصلات کو فعال کرتا ہے۔ یہ ایک معیاری مواصلاتی لیئر فراہم کرتا ہے جو پرسیپشن سسٹمز، کوگنیٹو آرکیٹیکچرز، کنٹرول الگورتھمز، اور VLA ماڈلز کو ایک مربوط روبوٹک سسٹم میں جوڑتا ہے۔

## ROS 2 کیا ہے؟

ROS 2 روبوٹ سافٹ ویئر لکھنے کے لیے ایک لچکدار فریم ورک ہے جو فراہم کرتا ہے:

- **تقسیم شدہ کمپیوٹنگ**: متعدد پروسیسز مختلف مشینوں پر چل سکتے ہیں
- **مواصلاتی مڈل ویئر**: DDS (ڈیٹا ڈسٹری بیوشن سروس) کا استعمال کرتے ہوئے معیاری پیغام رسانی
- **پیکج مینجمنٹ**: ڈیپینڈنسیز کے ساتھ منظم کوڈ ڈھانچہ
- **سمولیشن انٹیگریشن**: فزکس سمیولیٹرز کے ساتھ بغیر رکاوٹ کنکشن
- **ہارڈ ویئر ایبسٹریکشن**: مختلف روبوٹس اور سینسرز کے لیے متحد انٹرفیسز

![ROS2 آرکیٹیکچر](/img/flowdiagram4.jpg)

*تصویر: نوڈز، ٹاپکس، اور سروسز دکھاتے ہوئے ہیومنائیڈ روبوٹس کے لیے ROS2 مواصلاتی آرکیٹیکچر*

## ROS 2 انسٹال کرنا

ہیومنائیڈ روبوٹکس ڈیولپمنٹ کے لیے، ہم **ROS 2 Humble Hawksbill** (LTS ورژن) یا جدید ترین فیچرز کے لیے **Rolling Ridley** کی سفارش کرتے ہیں:

### اوبنٹو انسٹالیشن

```bash
# ROS 2 apt ریپوزٹری شامل کریں
sudo apt update && sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# ROS 2 پیکجز انسٹال کریں
sudo apt update
sudo apt install ros-humble-desktop
```

## اپنا پہلا روبوٹکس ورک اسپیس بنانا

ہیومنائیڈ روبوٹکس پروجیکٹس کے لیے، ایک ورک اسپیس ڈھانچہ بنائیں جو مختلف اجزاء کو الگ کرے:

```bash
# ورک اسپیس ڈائریکٹری بنائیں
mkdir -p ~/humanoid_ws/src
cd ~/humanoid_ws

# colcon ورک اسپیس بنائیں
colcon build
source install/setup.bash
```

## ہیومنائیڈ روبوٹکس کے لیے بنیادی ROS 2 تصورات

### نوڈز

نوڈز انفرادی پروسیسز ہیں جو روبوٹ فنکشنز انجام دیتے ہیں۔ ہیومنائیڈ روبوٹ کے لیے، آپ کے پاس ہو سکتے ہیں:

```python
# robot_perception/perception_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, JointState

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('humanoid_perception_node')

        # کیمرہ ڈیٹا کو سبسکرائب کریں
        self.camera_sub = self.create_subscription(
            Image,
            '/humanoid/camera/color/image_raw',
            self.camera_callback,
            10
        )

        self.get_logger().info('ہیومنائیڈ پرسیپشن نوڈ شروع ہوا')

    def camera_callback(self, msg):
        # آبجیکٹ ڈٹیکشن کے لیے کیمرہ امیج پروسیس کریں
        self.get_logger().info(f'کیمرہ امیج موصول: {msg.width}x{msg.height}')
```

### ٹاپکس اور میسجز

ٹاپکس نامزد بسیں ہیں جن پر نوڈز پیغامات کا تبادلہ کرتے ہیں۔ ہیومنائیڈ روبوٹکس کے لیے، عام ٹاپکس میں شامل ہیں:

- `/humanoid/joint_states` - جوائنٹ پوزیشنز اور ویلوسٹیز
- `/humanoid/camera/color/image_raw` - کیمرہ امیجز
- `/humanoid/imu` - IMU سینسر ڈیٹا

### سروسز

سروسز ہم وقت ساز آپریشنز کے لیے درخواست-جواب مواصلات فراہم کرتی ہیں۔

## ہیومنائیڈ مخصوص نوڈز بنانا

### VLA انٹیگریشن نوڈ

```python
# robot_vla/vla_integration_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class VLAIntegrationNode(Node):
    def __init__(self):
        super().__init__('vla_integration_node')

        # سبسکرپشنز
        self.image_sub = self.create_subscription(
            Image, '/humanoid/camera/rgb/image_raw',
            self.image_callback, 10
        )

        self.get_logger().info('VLA انٹیگریشن نوڈ شروع ہوا')
```

## ہیومنائیڈ روبوٹکس کے لیے بہترین طریقے

1. **مستقل نامکاری کنونشنز استعمال کریں**: `/humanoid/<subsystem>/<topic_name>`
2. **مناسب ایرر ہینڈلنگ نافذ کریں**: جب اجزاء ناکام ہوں تو سنبھالنا
3. **سسٹم کی کارکردگی مانیٹر کریں**: CPU، میموری، اور نیٹ ورک کا استعمال
4. **حفاظتی میکانزمز نافذ کریں**: ایمرجنسی اسٹاپس اور حدود
5. **اہم واقعات لاگ کریں**: ڈیبگنگ اور تجزیے کے لیے

ROS 2 پیچیدہ ہیومنائیڈ روبوٹکس سسٹمز کو مربوط کرنے کے لیے ضروری انفراسٹرکچر فراہم کرتا ہے، ایک متحد فریم ورک میں پرسیپشن، کوگنیشن، ایکشن، اور مواصلات کے انضمام کو فعال کرتا ہے۔
