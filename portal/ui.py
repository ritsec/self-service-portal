from flask import (
    Blueprint
)

bp = Blueprint('ui', __name__)


##
#   Routes
##
@bp.route('/', methods=['GET'])
def index():
    return 'hello!'
