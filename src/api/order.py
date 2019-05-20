from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from src.db.model import db, Orders

bp = Blueprint('order', __name__, url_prefix='/apis')


@bp.route('/order/mainOrder', methods=('GET', 'POST'))
def solve_mainOrder():
    if request.method == 'POST':
        task = request.form['task']
        return task
    elif request.method == 'GET':
        return "hello"