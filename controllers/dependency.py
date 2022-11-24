# -*- coding: utf-8 -*-
from core.exception import ErrorMessage
from flask import request
from flask import Blueprint
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from utils.converter import to_int
from models.degree import Degree

blueprint = Blueprint('dependency', __name__, template_folder='templates')

@blueprint.route('/dependency', methods=['GET'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('dependency.html')
def dependency():
    degrees = Degree.get_all_degrees()
    selected_degree_index = to_int(request.args.get('index', 1), 'index')
    if selected_degree_index < 0 or selected_degree_index > len(degrees):
        selected_degree_index = 0
    return {
        'degrees': degrees,
        'selected_index': selected_degree_index}