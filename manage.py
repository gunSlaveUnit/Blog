from flask import Flask

from web.base.routes import base

app = Flask(__name__)
app.register_blueprint(base)


if __name__ == '__main__':
    app.run(debug=True)
