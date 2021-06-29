# WARNING: DON'T TOUCH NOTHING HERE!
from services import app
from web.base.routes import base
from web.users.routes import users
from web.posts.routes import posts
from web.errors.handlers import errors


app.register_blueprint(base)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(errors)


if __name__ == '__main__':
    app.run(debug=True)
