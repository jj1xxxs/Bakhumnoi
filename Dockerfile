# ใช้ Python เวอร์ชัน 3.11 (เป็นมาตรฐานและเสถียร)
FROM python:3.11-slim

# กำหนดโฟลเดอร์ทำงานใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt มาติดตั้งก่อน (เพื่อความเร็วในการ Build)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมดในโฟลเดอร์นี้เข้าไปใน container
COPY . .

# เปิดพอร์ต 5000 สำหรับ Railway
EXPOSE 5000

# รันบอทด้วย Gunicorn (เชื่อมต่อกับไฟล์ app.py และตัวแปร app)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
