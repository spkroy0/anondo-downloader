# পাইথন ইমেজ ব্যবহার করা হচ্ছে
FROM python:3.10-slim

# লিনাক্স আপডেট এবং GCC ইন্সটল করা
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# কাজের ডিরেক্টরি
WORKDIR /app

# ফাইলগুলো কপি করা
COPY . .

# লাইব্রেরি ইন্সটল করা
RUN pip install --no-cache-dir -r requirements.txt

# পোর্ট এক্সপোজ করা (Render এর জন্য)
EXPOSE 5000

# অ্যাপ রান করা
CMD ["python", "app.py"]
