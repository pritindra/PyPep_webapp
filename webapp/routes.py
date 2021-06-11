from flask import Blueprint
from . import controllers


# e.g blueprint and routes
auth_blueprint = Blueprint("auth",__name__, template_folder="templates", static_folder='static')
# auth_blueprint.add_url_rule("register", "register", controllers.register)
# auth_blueprint.add_url_rule("login", "login", controllers.login)

@auth_blueprint.route('/register')
def register():

    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    usr = User(username = username)
    usr.hash_password(password)
    db.session.add(usr)
    db.session.commit()