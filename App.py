import os
from flask import Flask, render_template, make_response, jsonify
from flask_compress import Compress

app = Flask(__name__)

# সাইট সুপার ফাস্ট করার জন্য Gzip কম্প্রেশন
Compress(app)

# কনফিগুরেশন: স্ট্যাটিক ফাইল ক্যাশিং (১ বছর)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    """
    মেইন এডিটর পেজ লোড এবং সিকিউরিটি হেডার সেটআপ।
    """
    response = make_response(render_template('index.html'))
    # অ্যাডভান্সড সিকিউরিটি হেডারস
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Server'] = 'Anondo Pro RGB Server 2.0'
    return response

# এরর হ্যান্ডলিং - ৪0৪
@app.errorhandler(404)
def page_not_found(e):
    return """
    <body style="background:#0b1120; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; flex-direction:column; text-align:center;">
        <h1 style="color:#ef4444; font-size:50px;">404</h1>
        <p style="font-size:20px;">Oi bhai, vul rasta e aisa porson!</p>
        <a href="/" style="margin-top:20px; color:#38bdf8; text-decoration:none; border:1px solid #38bdf8; padding:10px 25px; border-radius:30px; transition:0.3s;">Home e Fire Jao</a>
    </body>
    """, 404

# সার্ভার রান করার লজিক
if __name__ == "__main__":
    # Render বা Heroku এর পজিশন অনুযায়ী পোর্ট অটো-ডিটেকশন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
