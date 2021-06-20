from flask import Flask

from web.base.routes import base
from web.users.routes import users

app = Flask(__name__)
app.config['SECRET_KEY'] = \
    '176cec908f34145d2befd36987ad19b'

app.register_blueprint(base)
app.register_blueprint(users)


if __name__ == '__main__':
    app.run(debug=True)
