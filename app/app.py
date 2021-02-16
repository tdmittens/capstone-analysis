# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

from flask import Flask, render_template, request,  redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
