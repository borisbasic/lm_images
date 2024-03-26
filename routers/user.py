from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database.models import DbImages, DbEvents
from typing import List
from routers.schemas import UsersPics, UserAuth, DownloadPics
from auth.oauth2 import get_current_user
from dotenv import load_dotenv
import os, tarfile, shutil
load_dotenv()
BASE_URL = os.environ.get('BASE_URL_LM') 

def check_user(role: str):
    if role != 'user':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can not access here",
        )

def check_root_image(path):
    if not os.path.isfile(path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No image. Try another one.",
        )
    
router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get('/pics', response_model=List[UsersPics])
def get_users_pics(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_user(current_user.role)
    event = db.query(DbEvents).filter(DbEvents.user_id == current_user.id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event not found",
        )
    return event.images


@router.post('/download')
def download_images(request: DownloadPics, current_user: UserAuth = Depends(get_current_user)):
    check_user(current_user.role)
    path = f'{BASE_URL}images/{current_user.username}'
    if os.path.isfile(f'{path}.tar.gz'):
        os.remove(f'{path}.tar.gz')
    if len(request.images) == 1:
        check_root_image(path=f'{path}/{request.images[0]}')
            
        return FileResponse(path=f'{path}/{request.images[0]}', 
                            media_type='image/jpg',
                            filename=request.images[0])
    for ri in request.images:
        check_root_image(f'{path}/{ri}')
    with tarfile.open(f'{path}.tar.gz', 'w:gz') as tar:
        for root, _, files in os.walk(path):
            for file in files:
                if file in request.images:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, path)
                    tar.add(file_path, arcname=arcname)

    return FileResponse(path=f'{BASE_URL}images/{current_user.username}.tar.gz',
                        filename=f'{current_user.username}.tar.gz', 
                        media_type='application/x-tar')
    