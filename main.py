import os
from flask import Flask, render_template, redirect, send_from_directory
from flask import request, abort
from werkzeug import exceptions
from forms.search_forms import FileForm
import random
from file_conv import important_changer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KJKjxkwh7w6%575&jBHJI(987'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024
UPLOADED_MANUALS_ALLOW = ('pdf',)
app.config['UPLOAD_FOLDER'] = 'static/img/'


# <handler> Login, error handling via Flask
@app.errorhandler(exceptions.BadRequest)
def handle_401(_):
    return render_template('error.html', error=401)


@app.errorhandler(exceptions.BadRequest)
def handle_403(_):
    return render_template('error.html', error=403)


@app.errorhandler(exceptions.BadRequest)
def handle_404(_):
    return render_template('error.html', error=404)


@app.errorhandler(exceptions.BadRequest)
def handle_500(_):
    return render_template('error.html', error=500)


app.register_error_handler(401, handle_401)
app.register_error_handler(403, handle_403)
app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    fa_form = FileForm()
    if fa_form.filedata.data:
        num = str(random.randint(10000000000, 99999999999))
        manual_path = ''.join([
            app.config['UPLOAD_FOLDER'],
            num, '.pdf'
        ])
        fa_form.filedata.data.save(manual_path)
        important_changer(manual_path, param=fa_form.on_display_at.data)
        return render_template('main.html', form=fa_form, filename=f'{num}.pdf.docx', webview_title='iLegal main')
    return render_template('main.html', form=fa_form, webview_title='iLegal main')


@app.route('/info')
def info():
    return render_template('info.html', webview_title='About iLegal')


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print(filename)
    try:
        print(app.config['UPLOAD_FOLDER'])
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'missing.png', as_attachment=True)
    except Exception as e:
        print('huh')
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
