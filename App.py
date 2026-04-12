import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
