# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask.helpers import flash, url_for
from core.lang import get_str
from core.exception import ErrorMessage
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from models.course import Course
from models.cilo import CILO

blueprint = Blueprint('search', __name__, template_folder='templates')


@blueprint.route('/search', methods=['GET', 'POST'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('search.html')
def search():
    pass


@blueprint.route('/search/result', methods=['GET', 'POST'])
@restricted_access(allowed=[STUDENT, LECTURER, COURSE_DESIGNER])
@render_context('search_results.html')
def search_result():
    search_type = request.args.get('type', None)
    search_keyword = request.args.get('keyword', None)

    if search_type is None:
        raise ErrorMessage(get_str('SEARCH_TYPE_EMPTY'))
    if search_keyword is None:
        raise ErrorMessage(get_str('SEARCH_KEYWORD_EMPTY'))

    if search_type == 'course':
        return {
            'courses': Course.find_course_by_keyword(search_keyword), 
            'search_type': search_type}
    elif search_type == 'cilo':
        cilos = CILO.find_cilo_by_keyword(search_keyword)
        courses = []
        for cilo in cilos:
            courses.append(Course.find_course_by_id(cilo.course_id))
        return {
            'cilos': cilos, 
            'courses': courses, 
            'search_type': search_type}
    elif search_type == 'keyword':
        results = Course.find_courses_cilo_by_keyword(keyword=search_keyword)
        courses = [result[0] for result in results]
        cilos = [result[1] for result in results]
        return {
            'cilos': cilos, 
            'courses': courses, 
            'search_type': search_type}
    else:
        flash(get_str('INVALID_SEARCH_TYPE'))
        return redirect(url_for('search.search'))