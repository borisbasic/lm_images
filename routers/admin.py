from fastapi import APIRouter, status, HTTPException
from routers.schemas import GetEvent, PostUser
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database.models import DbUser, DbCategories, DbEvents, EventCategories
from database.hashing import Hash
from typing import List
from auth.oauth2 import get_current_user
import uuid, os, shutil, qrcode
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.environ.get('BASE_URL_LM')
APP_URL = os.environ.get('APP_URL_LM')
def check_admin(role: str):
    if role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can not access here",
        )
def delete_super_admin(role: str):
    if role == 'super-admin' or role == 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can not delete",
        )


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.post('/user')
def post_user(request: PostUser, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    check_admin(current_user.role)
    new_user = db.query(DbUser).filter(DbUser.username == request.username).first()
    category = db.query(DbCategories).filter(DbCategories.id == request.events.categories.id).first()
    if new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User exists",
        )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such category",
        )
    new_user = DbUser(
        username = request.username,
        password = Hash.bcrypt(request.password),
        email = request.email,
        role = 'user'
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    qr_uuid = uuid.uuid4().hex
    event = DbEvents(
        event = request.events.event,
        date = request.events.date,
        qr_code_uuid = qr_uuid,
        user_id = new_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    event_category = EventCategories(
        event_id = event.id,
        category_id = category.id
    )
    db.add(event_category)
    db.commit()
    db.refresh(event_category)
    user_dir = f'{BASE_URL}images/{new_user.username}'
    if not os.path.isdir(f'{BASE_URL}images/{new_user.username}'):
        os.mkdir(user_dir)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    data =  f'{APP_URL}{qr_uuid}'
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save(f'{BASE_URL}images/{event.users.username}/{qr_uuid}.jpg')
    return {'message': 'User added'}




@router.get('/events', response_model=List[GetEvent])
def get_events(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    check_admin(current_user.role)
    events = db.query(DbEvents).all()
    return events


@router.delete('/user/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    check_admin(current_user.role)
    user = db.query(DbUser).filter(DbUser.id == id).first()
    delete_super_admin(user.role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not exists",
        )
    shutil.rmtree(f'{BASE_URL}/images/{user.username}')
    db.delete(user)
    db.commit()
    
    return {'message': 'User deleted'}


    
