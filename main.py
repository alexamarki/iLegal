import os
from flask import Flask, render_template, redirect, send_file
from flask import request
from werkzeug import exceptions
from forms.search_forms import FileForm
import random

# ! ! ! ! ! ! ! ! ! ! ! ! ! Comment clarification ! ! ! ! ! ! ! ! ! ! ! ! ! #
# This is ArtHeritage's main file, which includes all routes and the         #
#   majority of the logic required for our Flask web app.                    #
# This file in particular is commented in the following manner:              #
# --Use case 1--                                                             #
# | [code] # comment - a comment regarding a particular portion of the code, #
#                          when it's written on the same line as the code.   #
# | # > comment - the aforementioned use case, when written on a blank line. #
# --Use case 2--                                                             #
# | # '--' * n <tag> comment                                                 #
# In use case #2, <tag> is either an opening or a closing tag.               #
#   These tags are always used in pairs (<tag>code</tag>).                   #
# * Tags in our comments surround code related to a particular portion of    #
#       the app, and are supposed to improve code readability, as well as    #
#       ease troubleshooting.                                                #
# * Next to the opening tag is a comment, explaining the purpose of the code #
#       it envelops.                                                         #
# * '--' may also be used n times (n >= 0) in the beginning of a comment to  #
#       clarify the level of indentation.                                    #
# As such, the following pseudocode...                                       #
# 01| # <tag1> Tag 1 explanation                                             #
# 02| # -- <tag1-1> Tag 1.1 explanation                                      #
# 03| def foo():                                                             #
# 04|   pass                                                                 #
# 05| # -- </tag1-1>                                                         #
# 06| # -- <tag1-2> Tag 1.2 explanation                                      #
# 07| def bar():                                                             #
# 08|   pass                                                                 #
# 09| # -- </tag1-2>                                                         #
# 10| # </tag1>                                                              #
# 11| # <tag2> Tag 2 explanation                                             #
# 12| def baz():                                                             #
# 13|   pass                                                                 #
# 14| # </tag2>                                                              #
# ...would tell us that foo() holds the properties of tags 1 and 1.1,        #
#   bar() holds the properties of tags 1 and 1.2,                            #
#   and baz() holds the property of tag 2                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KJKjxkwh7w6%575&jBHJI(987'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/static/img'



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
        file = fa_form.filedata.data
        num = random.randint(10000000000, 99999999999)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "\pdf\\", f'f{num}'))
        # call file creator
        return render_template('main.html', form=fa_form, filename=f'f{num}_edit', webview_title='iLegal main')
    return render_template('main.html', form=fa_form, webview_title='iLegal main')


@app.route('/info')
def info():
    return render_template('info.html', webview_title='About iLegal')


@app.route('/download/<string:file>')
def download(file):
    return send_file(file, as_attachment=True)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
