# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from core.engine import render_context
from core.lang import get_str
from core.exception import ErrorMessage
from core.permission import restricted_access
from models.user import ROLE_TYPE_ADMIN
from models.user import ROLE_TYPE_USER
from models.task import Task
from utils.converter import to_int
from utils.pagination import get_page_numbers

blueprint = Blueprint('tasks', __name__, template_folder='templates')


@blueprint.route('/tasks', methods=['GET'])
@restricted_access(allowed=[ROLE_TYPE_ADMIN, ROLE_TYPE_USER])
@render_context('tasks.html')
def tasks():
    page = request.args.get('page', 1)
    page_size = 10
    tasks, count = Task.get_user_tasks(session.get('user_id'), use_pagination=True, page_size=page_size, page=to_int(page))
    return {
        'tasks': tasks,
        'pages': get_page_numbers(length=count, current=page, limit=page_size, show=8),
        'current_page': str(page)
    }


# @blueprint.route('/courses/add', methods=['POST'])
# @render_context('courses.html', commit_on_success=False, rollback_on_exception=False)
# def add_course():
#     # Deprecated function. Should no longer be used.
#     # Moved to APIs
#     if request.method == 'POST':
#         content = request.get_json()
#         Course.add_course(content)
#         flash(get_str('CREATED', obj_name=get_str('ACOURSE')))


# @blueprint.route('/courses/edit', methods=['POST'])
# @render_context('courses.html', commit_on_success=True, rollback_on_exception=True)
# def modify_course():
#     # Deprecated function. Should no longer be used.
#     # Moved to APIs
#     if request.method == 'POST':
#         content = request.get_json()
#         course = Course.find_course_by_id(content['course_id'])
#         if course is None:
#             raise ErrorMessage(get_str('NOT_FOUND_OBJECT', object_name='course'))
#         course.modify_course(content)


# @blueprint.route('/courses/', methods=['GET', 'POST'])
# def empty_redirect():
#     return redirect(url_for('courses.courses'))
