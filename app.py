from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    # فحص الملف باستخدام ClamWin عبر سطر الأوامر (تأكد أن clamscan موجود في PATH)
    try:
        # Run clamscan on the uploaded file
        result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
        
        # Print the result to the console for debugging
        print(result.stdout)
        
        # إذا كان الفحص إيجابيًا للفيروسات، فإن النتيجة ستحتوي على كلمة "FOUND"
        if 'FOUND' in result.stdout:
            virus_name = result.stdout.split(':')[1].strip()
            return jsonify({"status": "infected", "virus": virus_name}), 200
        else:
            return jsonify({"status": "clean"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
