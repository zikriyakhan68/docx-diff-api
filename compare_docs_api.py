import base64
import io
from flask import Flask, request, jsonify
from docx import Document
import difflib

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare_docs():
    try:
        data = request.get_json()
        old_b64 = data['old_base64']
        new_b64 = data['new_base64']

        old_bytes = base64.b64decode(old_b64)
        new_bytes = base64.b64decode(new_b64)

        old_doc = Document(io.BytesIO(old_bytes))
        new_doc = Document(io.BytesIO(new_bytes))

        old_text = "\n".join([para.text for para in old_doc.paragraphs])
        new_text = "\n".join([para.text for para in new_doc.paragraphs])

        diff = "\n".join(difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile='old.docx',
            tofile='new.docx'
        ))

        return jsonify({'diff': diff})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
