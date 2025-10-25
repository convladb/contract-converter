from flask import Flask, render_template, request, send_file
from docx import Document
import os

app = Flask(__name__)

def docx_to_text(file_path):
    doc = Document(file_path)
    text_lines = []
    for para in doc.paragraphs:
        text_lines.append(para.text)
    return "\n".join(text_lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if not file.filename.endswith('.docx'):
        return "Загрузите файл .docx", 400

    file_path = os.path.join("temp.docx")
    file.save(file_path)

    text = docx_to_text(file_path)
    txt_path = "result.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    os.remove(file_path)
    return send_file(txt_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
