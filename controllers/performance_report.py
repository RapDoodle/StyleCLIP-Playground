# -*- coding: utf-8 -*-
from core.exception import ErrorMessage
from operator import index
from flask import Blueprint
from flask import session
from flask import request
from flask import flash
from core.lang import get_str
from core.engine import render_context
from core.permission import restricted_access
from core.permission import STUDENT
from core.permission import LECTURER
from core.permission import COURSE_DESIGNER
from utils.converter import to_int
from models import student_report
from models.course import Course
from models.report import Report
from models.student_report import StudentReport

blueprint = Blueprint('performance_report', __name__, template_folder='templates')


@blueprint.route('/performance', methods=['GET'])
@restricted_access(allowed=[STUDENT])
@render_context('performance_report.html')
def report():
    reports = Report.get_student_completed_courses(session['user_id'])
    completed_courses = [x[0] for x in reports]
    n = len(completed_courses)
    index = to_int(request.args.get('index', 0), 'index')
    cilos = []
    scores = []
    if n > 0:
        if index >= 0 and index < n:
            # Get the index in the student's completed course list
            scores = reports[index][2].get_cilo_performance()
            version = reports[index][1].get_course_version()
            course = reports[index][0]
            cilos = course.get_cilos(course_version_id=version.id)
        else:
            raise ErrorMessage(get_str('INVALID_INDEX'))
    return {
        'completed_courses': completed_courses,
        'index': index,
        'scores': scores,
        'cilos': cilos
    }

