# -*- coding: utf-8 -*-
import os
import re
import json
import uuid
import base64
import hashlib
from datetime import timedelta

from sqlalchemy.sql import func

import models
from core.db import db
from core.exception import ErrorMessage
from models.user import User
from models.task_log import TaskLog
from utils.converter import to_int


TASK_TYPE_UNKNOWN = 0
TASK_TYPE_LATENT_VECTOR_OPTIMIZATION = 1
TASK_TYPE_LATENT_MAPPER = 2
TASK_TYPE_GLOBAL_DIRECTION = 3
VALID_TASK_TYPES = [TASK_TYPE_LATENT_VECTOR_OPTIMIZATION, TASK_TYPE_LATENT_MAPPER, TASK_TYPE_GLOBAL_DIRECTION]

TASK_STATUS_PENDING = 0
TASK_STATUS_RUNNING = 1
TASK_STATUS_FINISHED = 2
TASK_STATUS_ERROR = 3
VALID_TASK_STATUS = [TASK_STATUS_PENDING, TASK_STATUS_RUNNING, TASK_STATUS_FINISHED, TASK_STATUS_ERROR]

class Task(models.saveable_model.SaveableModel):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_uuid = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_title = db.Column(db.String(128))
    task_type = db.Column(db.Integer)
    task_parameters = db.Column(db.String(36))
    task_output = db.Column(db.String(36))
    task_status = db.Column(db.Integer)
    input_file = db.Column(db.String(128))
    output_file = db.Column(db.String(128))
    task_parameters = db.Column(db.String(36))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, task_type, task_parameters, task_title=None, task_status=TASK_STATUS_PENDING):
        super().__init__()

        # Clean and validate the data
        user_id = to_int(str(user_id).strip())
        task_type = to_int(str(task_type).strip())
        if task_title is None:
            task_title = 'Untitled task'
        task_title = task_title.strip()
        if task_type not in VALID_TASK_TYPES:
            raise ErrorMessage('Invalid task type')
        task_parameters = json.dumps(task_parameters, indent=None)
        task_status = to_int(str(task_status).strip())
        if task_status not in VALID_TASK_STATUS:
            raise ErrorMessage('Invalid task status')

        # Store the data in the object
        self.user_id = user_id
        self.task_uuid = uuid.uuid4().hex
        self.task_type = task_type
        self.task_title = task_title
        self.task_parameters = task_parameters
        self.task_status = task_status

    def get_user_id(self):
        return self.user_id

    def get_time_created_local_time(self):
        # TODO: Add support for all timezones. Currently, only Beijing/Hong Kong time is supported
        return self.time_created + timedelta(hours=8)

    def set_input_image(self, base64_str):
        md5 = hashlib.md5(base64_str.encode()).hexdigest()
        meta_info, base64_img = base64_str.split(',')
        file_extension = re.search(r'(?<=/)[a-zA-Z0-9]+(?=;)', meta_info).group()
        filename = f'{md5}.{file_extension}'
        img_path = os.path.join('.', 'static', 'contents', 'uploads', filename)
        if not os.path.exists(img_path):
            with open(img_path, 'wb') as f:
                f.write(base64.b64decode((base64_img)))
        self.input_file = filename

    def get_task_parameters(self, display_mode=False):
        task_parameters = json.loads(str(self.task_parameters))
        if display_mode:
            keys = list(task_parameters.keys())
            for key in keys:
                new_key = ' '.join([x.capitalize() for x in key.split('_')])
                if new_key != key:
                    task_parameters[new_key] = task_parameters[key]
                    del task_parameters[key]

        return task_parameters

    def get_task_type_string(self):
        if self.task_type == TASK_TYPE_LATENT_VECTOR_OPTIMIZATION:
            return 'Latent Vector Optimization'
        elif self.task_type == TASK_TYPE_LATENT_MAPPER:
            return 'Latent Mapper'
        elif self.task_type == TASK_TYPE_GLOBAL_DIRECTION:
            return 'Global Direction'
        else:
            return 'Unknown'

    def get_task_status_string(self):
        if self.task_status == TASK_STATUS_PENDING:
            return 'Pending'
        elif self.task_status == TASK_STATUS_RUNNING:
            return 'Running'
        elif self.task_status == TASK_STATUS_FINISHED:
            return 'Finished'
        elif self.task_status == TASK_STATUS_ERROR:
            return 'Error'
        else:
            return 'Unknown'

    def get_task_log(self):
        return TaskLog.find_task_log_by_task_id(self.id)

    @classmethod
    def find_task_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_pending_tasks(cls):
        return cls.query.filter_by(task_status=TASK_STATUS_PENDING)\
            .order_by(cls.time_created.asc()).all()

    @classmethod
    def get_running_tasks(cls):
        return cls.query.filter_by(task_status=TASK_STATUS_RUNNING)\
            .order_by(cls.time_created.asc()).all()

    @classmethod
    def get_user_tasks(cls, user_id, use_pagination=False, page_size=20, page=1):
        task_query = cls.query.filter_by(user_id=user_id).order_by(cls.time_created.desc())
        if use_pagination:
            count = task_query.count()
            tasks = task_query.limit(page_size).offset((page-1)*page_size).all()
            return tasks, count
        else:
            return task_query.all() 