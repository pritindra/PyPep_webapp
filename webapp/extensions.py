from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .models import *


from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()