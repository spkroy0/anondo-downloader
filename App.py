import os
from flask import Flask, render_template, make_response
from flask_compress import Compress # সাইট ফাস্ট করার জন্য

app = Flask(__name__)

# প্রিমিয়াম ফিচার: সাইটের সব ডেটা কম্প্রেস করবে যাতে দ্রুত লোড হয়
Compress(app)

# সিকিউরিটি কনফিগুরেশন
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000 # ক্যাশে মেমোরি অপ্টিমাইজেশন

@app.route('/')
def index():
    """
    মেইন এডিটর পেজ লোড করবে। 
    এখানে কিছু প্রিমিয়াম রেসপন্স হেডার যোগ করা হয়েছে।
    """
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN' # সিকিউরিটি হেডার
    response.headers['Server'] = 'Anondo Pro Server 1.0' # কাস্টম সার্ভার নাম
    return response

# প্রিমিয়াম ৪0৪ পেজ (যদি কেউ ভুল লিঙ্কে যায়)
@app.errorhandler(404)
def page_not_found(e):
    return """
    <body style="background:#0b1120; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; flex-direction:column;">
        <h1 style="color:#38bdf8;">404 - Lost in Code?</h1>
        <p>Oi bhai, vul rasta e aisa porson! Link check koro.</p>
        <a href="/" style="color:#38bdf8; text-decoration:none; border:1px solid #38bdf8; padding:10px 20px; border-radius:5px;">Home e Fire Jao</a>
    </body>
    """, 404

if __name__ == "__main__":
    # পোর্ট অটো-ডিটেকশন (Render/Heroku এর জন্য)
    port = int(os.environ.get("PORT", 5000))
    
    # প্রোডাকশন মোডে রান করা
    app.run(host='0.0.0.0', port=port, debug=False)
