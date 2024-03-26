from fastapi import APIRouter, status, HTTPException, Request, UploadFile, File
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database.models import DbUser, DbOtherUsers, DbEvents, DbImages
from typing import List
from routers.schemas import OthesUserInfo
import os, shutil, uuid
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ.get('BASE_URL_LM')

router = APIRouter(
    prefix='/other-user',
    tags=['other-user']
)

@router.get('/{event_uuid}')
def get_other_user_info(event_uuid: str, request: Request, db: Session = Depends(get_db)):
    other_user_device = request.headers.get('User-Agent')
    client_ip = request.client.host
    event_id = db.query(DbEvents).filter(DbEvents.qr_code_uuid == event_uuid).first()
    event_id = event_id.id
    other_user = db.query(DbOtherUsers).filter(DbOtherUsers.device_name == other_user_device).first()
    if not other_user:
        other_user = DbOtherUsers(
            device_name = other_user_device,
            device_ip = client_ip,
            event_id = event_id
        )
        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        return {'message': 'You have 10 images to upload.'}
    
    num_of_img = db.query(DbImages).filter(DbImages.other_users_id == other_user.id).count()
    if num_of_img < 10:
        allowed = 10-num_of_img
        return {'message': f'You have {allowed} images to upload'}
    return {'message': 'You have no more messages to upload.'}


@router.post('/upload-image-event/{event_uuid}/{img_to_upload}')
def upload_image_event(event_uuid: str, img_to_upload: int, request: Request,images: list[UploadFile] = File(...),  db: Session = Depends(get_db)):
    event = db.query(DbEvents).filter(DbEvents.qr_code_uuid == event_uuid).first()
    event_id = event.id
    event_username = event.users.username
    other_user_device = request.headers.get('User-Agent')
    other_user_id = db.query(DbOtherUsers).filter(DbOtherUsers.device_name == other_user_device).first().id
    client_ip = request.client.host
    if len(images)>img_to_upload:
        return {'message': f'You can upload only {img_to_upload} images'}
    for img in images:
        img_name = uuid.uuid4().hex
        with open(f'{BASE_URL}images/{event_username}/{img_name}.jpg', 'w+b') as buffer:
            shutil.copyfileobj(img.file, buffer)
        new_img = DbImages(
            image_name = img_name+'.jpg',
            event_id = event_id,
            other_users_id = other_user_id
        )
        db.add(new_img)
        db.commit()
        db.refresh(new_img)

    return {'message': 'uploaded'}
