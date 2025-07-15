from flask import Flask, request, jsonify
from docx import Document
import tempfile
import os
import difflib

app = Flask(__name__)

def get_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

@app.route('/compare', methods=['POST'])
def compare_docs():
    if 'old' not in request.files or 'new' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    old_file = request.files['old']
    new_file = request.files['new']

    with tempfile.NamedTemporaryFile(delete=False) as f1:
        f1.write(old_file.read())
        old_path = f1.name

    with tempfile.NamedTemporaryFile(delete=False) as f2:
        f2.write(new_file.read())
        new_path = f2.name

    old_text = get_text_from_docx(old_path)
    new_text = get_text_from_docx(new_path)

    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile='Previous Version',
        tofile='Current Version',
        lineterm=''
    )
    result = '\n'.join(diff)

    os.remove(old_path)
    os.remove(new_path)

    return jsonify({'diff': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
