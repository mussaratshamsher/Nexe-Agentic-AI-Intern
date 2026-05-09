---
sidebar_position: 2
---

# روبوٹکس سسٹمز کے لیے تکنیکی دستاویزات بنانا

مؤثر تکنیکی دستاویزات روبوٹکس پروجیکٹس کے لیے بہت اہم ہیں، جہاں کثیر الشعبہ ٹیموں کو تعاون کرنا اور پیچیدہ نظاموں کو سمجھنا ضروری ہے۔ Docusaurus آپ کو جامع دستاویزات بنانے کی اجازت دیتا ہے جو تکنیکی وضاحتیں، ریاضیاتی تصورات، کوڈ کی مثالیں، اور تجرباتی نتائج کو یکجا کرتی ہیں۔

## روبوٹکس تصورات کے لیے دستاویزات بنانا

اپنے روبوٹ سب سسٹم کے لیے `docs/actuators/servo-control.md` پر ایک Markdown فائل بنائیں:

```md title="docs/actuators/servo-control.md"
---
sidebar_position: 3
title: سروو موٹر کنٹرول
---

# سروو موٹر کنٹرول سسٹمز

سروو موٹرز بند لوپ سسٹمز ہیں جو روبوٹک جوائنٹس کے لیے درست زاویائی کنٹرول فراہم کرتے ہیں۔

## کنٹرول الگورتھم

```python
import numpy as np
import time

class ServoController:
    def __init__(self, kp=1.0, ki=0.1, kd=0.05):
        self.kp = kp  # تناسبی گین
        self.ki = ki  # انٹیگرل گین
        self.kd = kd  # مشتق گین
        self.prev_error = 0
        self.integral = 0

    def control_step(self, desired_angle, current_angle, dt):
        error = desired_angle - current_angle
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        output = (self.kp * error +
                 self.ki * self.integral +
                 self.kd * derivative)

        self.prev_error = error
        return np.clip(output, -1.0, 1.0)  # آؤٹ پٹ کو محفوظ حد تک محدود کریں
```

یہ ایک دستاویز بناتا ہے جو [http://localhost:3000/docs/actuators/servo-control](http://localhost:3000/docs/actuators/servo-control) پر قابل رسائی ہے۔

## دستاویز کی تنظیم کی حکمت عملی

روبوٹکس دستاویزات کے لیے، سسٹم کے اجزاء اور فعالیت کے مطابق دستاویزات کو ترتیب دیں:

```text
docs/
├── foundations/              # ریاضیاتی اور نظریاتی تصورات
│   ├── kinematics.md         # فارورڈ/انورس کائنیمیٹکس
│   ├── dynamics.md           # روبوٹ ڈائنامکس اور حرکت
│   └── control-theory.md     # کنٹرول سسٹمز تھیوری
├── hardware/                 # فزیکل اجزاء
│   ├── actuators.md          # موٹرز، سروز، ایکچویٹرز
│   ├── sensors.md            # IMU، کیمرے، انکوڈرز
│   └── computing.md          # آن بورڈ کمپیوٹرز اور پروسیسنگ
├── software/                 # الگورتھمز اور نفاذ
│   ├── perception.md         # آبجیکٹ ڈٹیکشن، SLAM
│   ├── planning.md           # پاتھ پلاننگ، موشن پلاننگ
│   └── control.md            # لو لیول اور ہائی لیول کنٹرول
└── applications/             # استعمال کے کیسز اور مظاہرے
    ├── manipulation.md       # آبجیکٹ مینی پولیشن ٹاسکس
    ├── locomotion.md         # چلنا، چڑھنا، حرکت
    └── human-interaction.md  # ہیومن-روبوٹ انٹریکشن
```

## روبوٹکس پروجیکٹس کے لیے سائیڈبار کی ترتیب

اپنے روبوٹکس سسٹم کی درجہ بندی والی ساخت کی عکاسی کرنے کے لیے `sidebars.js` میں اپنے سائیڈبار کی ترتیب دیں:

```js title="sidebars.js"
export default {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'سسٹم کی بنیادیں',
      items: [
        'foundations/core-concepts',
        'foundations/kinematics',
        'foundations/dynamics',
        'foundations/control-theory'
      ],
    },
    {
      type: 'category',
      label: 'ہارڈویئر اجزاء',
      items: [
        'hardware/actuators',
        'hardware/sensors',
        'hardware/computing'
      ],
    },
    {
      type: 'category',
      label: 'سافٹ ویئر اسٹیک',
      items: [
        'software/perception',
        'software/planning',
        'software/control'
      ],
    },
    {
      type: 'category',
      label: 'ایپلیکیشنز',
      items: [
        'applications/manipulation',
        'applications/locomotion',
        'applications/human-interaction'
      ],
    }
  ],
};
```

## روبوٹکس دستاویزات کے لیے بہترین طریقے

### ریاضیاتی فارمولیشنز شامل کریں

روبوٹکس میں اہم ریاضیاتی ماڈلنگ شامل ہے۔ مساواتوں کے لیے LaTeX استعمال کریں:

```md
## کائنیمیٹک مساواتیں

جوائنٹ اسپیس اور کارٹیشین اسپیس کے درمیان تعلق یہ ہے:

$$ \mathbf{x} = f(\mathbf{q}) $$

جہاں:
- $\mathbf{x}$ اینڈ ایفیکٹر پوز ویکٹر ہے
- $\mathbf{q}$ جوائنٹ اینگل ویکٹر ہے
- $f$ فارورڈ کائنیمیٹکس فنکشن کی نمائندگی کرتا ہے
```

### ویژولائزیشن فراہم کریں

تصورات کو واضح کرنے کے لیے ڈایاگرامز، سکیمیٹکس، اور تصاویر شامل کریں:

```md
![روبوٹ آرم کنفیگریشن](/img/chap3.jpg)

*تصویر: جوائنٹ لیبلنگ کے ساتھ عام 6-DOF روبوٹک مینی پولیٹر*
```

### سیاق و سباق کے ساتھ کوڈ کی دستاویزات بنائیں

ہمیشہ کوڈ کی مثالوں کا مقصد اور استعمال کا کیس بیان کریں:

```md
# جوائنٹ ٹریجیکٹری ٹریکنگ کے لیے PD کنٹرولر

یہ کنٹرولر مطلوبہ جوائنٹ ٹریجیکٹریز کو ٹریک کرنے کے لیے تناسبی-مشتق کنٹرول قانون نافذ کرتا ہے۔

```python
class PDController:
    def __init__(self, kp_vector, kd_vector):
        """
        ہر جوائنٹ کے لیے گینز کے ساتھ PD کنٹرولر شروع کریں
        :param kp_vector: تناسبی گینز [N⋅m/rad]
        :param kd_vector: مشتق گینز [N⋅m⋅s/rad]
        """
        self.kp = kp_vector
        self.kd = kd_vector

    def compute_torque(self, q_desired, q_actual, dq_desired, dq_actual):
        """
        PD قانون کا استعمال کرتے ہوئے کنٹرول ٹارک کا حساب لگائیں
        :param q_desired: مطلوبہ جوائنٹ پوزیشنز
        :param q_actual: اصل جوائنٹ پوزیشنز
        :param dq_desired: مطلوبہ جوائنٹ ویلوسٹیز
        :param dq_actual: اصل جوائنٹ ویلوسٹیز
        :return: ہر جوائنٹ کے لیے کنٹرول ٹارکس
        """
        position_error = q_desired - q_actual
        velocity_error = dq_desired - dq_actual
        tau = self.kp * position_error + self.kd * velocity_error
        return tau
```

یہ دستاویزات کا طریقہ آپ کے روبوٹکس پروجیکٹ میں نظریاتی سمجھ اور عملی نفاذ دونوں کے لیے وضاحت کو یقینی بناتا ہے۔
```

