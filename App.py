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

# Note: You can add your /py-editor route here following the same pattern
# as your index route.

if __name__ == "__main__":
    # Using environment variable for Port to ensure compatibility with hosting platforms
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
