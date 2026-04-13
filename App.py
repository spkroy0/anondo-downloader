import os
import subprocess
import uuid
from flask import Flask, render_template, make_response, request, jsonify
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

# টেম্পোরারি ফাইল রাখার ফোল্ডার তৈরি
TEMP_DIR = "temp_codes"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.route('/c-editor')
def c_editor():
    response = make_response(render_template('c_editor.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

# --- সি কোড কম্পাইল এবং রান করার নিজস্ব এপিআই ---
@app.route('/run-c', methods=['POST'])
def run_c_code():
    data = request.get_json()
    code = data.get('code', '')
    
    if not code:
        return jsonify({"output": "", "error": "No code provided!"}), 400

    unique_id = str(uuid.uuid4())
    source_file = os.path.join(TEMP_DIR, f"{unique_id}.c")
    output_exec = os.path.join(TEMP_DIR, f"{unique_id}.out")

    try:
        # ১. ইউজার থেকে পাওয়া কোডটি ফাইলে সেভ করা
        with open(source_file, "w") as f:
            f.write(code)

        # ২. GCC বা Clang দিয়ে কম্পাইল করা
        # নোট: সার্ভারে GCC না থাকলে Clang ট্রাই করবে
        compile_process = subprocess.run(
            ["gcc", source_file, "-o", output_exec],
            capture_output=True, text=True
        )

        if compile_process.returncode != 0:
            return jsonify({"output": "", "error": compile_process.stderr})

        # ৩. কম্পাইল করা ফাইলটি রান করা (৫ সেকেন্ড টাইমআউট যাতে সার্ভার ঝুলে না যায়)
        run_process = subprocess.run(
            [output_exec],
            capture_output=True, text=True, timeout=5
        )

        return jsonify({"output": run_process.stdout, "error": run_process.stderr})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Error: Execution Timeout (Possible Infinite Loop)"})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})
    finally:
        # ৪. কাজ শেষে টেম্পোরারি ফাইলগুলো মুছে ফেলা
        if os.path.exists(source_file): os.remove(source_file)
        if os.path.exists(output_exec): os.remove(output_exec)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
