from flask import (
    Blueprint
)

bp = Blueprint('account', __name__, url_prefix='/account')


##
#   Routes
##
@bp.route('/changePassword', methods=['POST'])
def change_password():
    # TODO
    pass


@bp.route('/register', methods=['POST'])
def create():
    # TODO
    pass


##
#   Helper functions
##
def verify_code(code):
    # TODO
    pass
