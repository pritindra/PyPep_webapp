from flask import Blueprint
from Bio.Seq import Seq
from controllers import *
 
# e.g blueprint and routes
auth_blueprint = Blueprint("auth",__name__, template_folder="ui/templates", static_folder='ui/static')
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

@auth_blueprint.route('/login')
def login(username,password):
    if username in user and check_password_hash(user.get(username), password):
        return username

@auth_blueprint.route('/sequencer')
def sequencer(seq):
    Inp = PepTool(str(seq).to_upper())
    # Sequencer logic here 

@auth_blueprint.route('/properties')
def properties(seq,pH):
    Inp = PepTool(str(seq).to_upper())
    print("The molecular weight of the sequence:: %0.2f" % Inp.molecular_weight())
    Inp.amino_count()
    Inp.isoelectric_point()
    Inp.charge_t_pH(pH)
    # Other properties here

@auth.blueprint.route('/home')
def home():
    return render_template('home.html')
