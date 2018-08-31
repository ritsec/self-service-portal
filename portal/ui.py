from flask import (
    Blueprint, render_template
)

bp = Blueprint('ui', __name__)


##
#   Routes
##
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
