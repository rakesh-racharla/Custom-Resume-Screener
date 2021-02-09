from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
if __name__ == "__main__":
    app.run()



a = 5

b=10

a+b
a-b

b%a

b/a

a*b

a==10
