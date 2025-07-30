import io
from flask import Flask, request, send_file
from flask_cors import CORS
from backgroundremover.bg import remove
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>الخادم يعمل على GitHub Codespaces!</h1>"


@app.route('/api/remove-background', methods=['POST'])
def remove_background_api():
    if 'file' not in request.files:
        return "خطأ: لم يتم إرسال ملف.", 400
    file = request.files['file']
    if file.filename == '':
        return "خطأ: لم يتم اختيار ملف.", 400
    try:
        input_bytes = file.read()
        output_bytes = remove(input_bytes, model_name="u2net")
        return send_file(
            io.BytesIO(output_bytes),
            mimetype='image/png'
        )
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return f"حدث خطأ أثناء معالجة الصورة: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
  
