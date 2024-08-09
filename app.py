import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024  # Limite de 2GB por arquivo

# Crie a pasta de uploads, se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica se o usuário enviou um arquivo
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Gera um nome único para o arquivo usando UUID
            filename = f"{uuid.uuid4()}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Gera um link para download
            download_link = url_for('download_file', filename=filename, _external=True)
            return render_template('index.html', download_link=download_link)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
