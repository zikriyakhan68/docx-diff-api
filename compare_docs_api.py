import base64
import io
import os
from flask import Flask, request, jsonify
from docx import Document
import difflib

app = Flask(__name__)

def get_text_from_docx_bytes(doc_bytes):
    doc = Document(io.BytesIO(doc_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

@app.route('/compare', methods=['POST'])
def compare_docs():
    try:
        data = request.get_json()
        old_b64 = data['old_base64']
        new_b64 = data['new_base64']

        old_bytes = base64.b64decode(old_b64)
        new_bytes = base64.b64decode(new_b64)

        old_text = get_text_from_docx_bytes(old_bytes)
        new_text = get_text_from_docx_bytes(new_bytes)

        diff = "\n".join(difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile='Previous Version',
            tofile='Current Version',
            lineterm=''
        ))

        return jsonify({'diff': diff})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
