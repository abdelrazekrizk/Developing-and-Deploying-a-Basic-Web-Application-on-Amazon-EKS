from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, this is a basic web application running on Amazon EKS!</p>"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
