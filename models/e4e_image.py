# -*- coding: utf-8 -*-
import models
from core.db import db
from models.user import User


class E4EImageLatent(models.saveable_model.SaveableModel):
    __tablename__ = 'e4e_image_latent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_md5 = db.Column(db.LargeBinary(16))
    latent_filename = db.Column(db.String(36))

    def __init__(self, img_md5, latent_filename):
        super().__init__()

        # Store the data in the object
        self.img_md5 = img_md5
        self.latent_filename = str(latent_filename).strip()

    def get_user_id(self):
        return self.user_id