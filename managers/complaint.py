import os

from constants import TEMP_FILE_FOLDER
from db import database
from models import complaint, RoleType, State
from services.s3 import S3Service
import uuid

from services.ses import SESService
from utils.helpers import decode_photo

s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        query = complaint.select()
        if user['role'] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user['id'])
        elif user['role'] == RoleType.approver:
            query = query.where(complaint.c.status == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data['photo_url'] = s3.upload(path, name, extension)

        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one((complaint.select().where(complaint.c.id == id_)))

    @staticmethod
    async def delete_complaint(id_):
        return await database.execute(complaint.delete().where(complaint.c.id == id_))

    @staticmethod
    async def approve(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.approved))
        ses.send_email("Complaint approved!", ["andrewnoa20@gmail.com"], "Congrats!")

    @staticmethod
    async def reject(id_):
        return await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.rejected))
