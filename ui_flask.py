from flask import Flask

app = Flask(__name__)

@app.route('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(port=8000,host='192.168.1.247')

