from fastapi import APIRouter, status, HTTPException
from routers.schemas import RegisterSuperAdmin, GetAllAdmins, \
    PostAdmin, UserAuth, PostCategory, GetCategory
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database.models import DbUser, DbCategories
from database.hashing import Hash
from typing import List
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/super-admin',
    tags=['super-admin']
)

def check_admin(role: str):
    if role != 'super-admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can not access here",
        )
    
def delete_super_admin(role: str):
    if role == 'super-admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can not delete",
        )

@router.post('/')
def register_super_admin(request: RegisterSuperAdmin, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User exists",
        )
    user = DbUser(username=request.username,
                  email=request.email,
                  password=Hash.bcrypt(request.password),
                  role='super-admin')
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'super-admin added'}
    
@router.get('/all-admins', response_model=List[GetAllAdmins])
def get_all_admins(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    admins = db.query(DbUser).filter(DbUser.role == 'admin').all()
    return admins


@router.post('/admin')
def post_admin(request: PostAdmin, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    admin = db.query(DbUser).filter(DbUser.username == request.username).first()
    if admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User exists",
        )
    admin = DbUser(username = request.username,
                   email = request.email,
                   password = Hash.bcrypt(request.password),
                   role = 'admin')
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {'message': 'Admin added'}


@router.delete('/admin/{id}')
def delete_admin(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    user = db.query(DbUser).filter(DbUser.id == id).first()
    delete_super_admin(user.role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User exists",
        )
    db.delete(user)
    db.commit()
    return {'message': 'Admin deleted'}

@router.post('/category')
def post_category(request: PostCategory, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    category = db.query(DbCategories).filter(DbCategories.category == request.category).first()
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category exists",
        )
    category = DbCategories(category = request.category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return {'message': 'category added'}

@router.put('/category/{id}')
def change_name_category(id: int,request: PostCategory, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    category = db.query(DbCategories).filter(DbCategories.id == id).first()
    category.category = request.category
    db.add(category)
    db.commit()
    db.refresh(category)
    return {'message': 'category updated'}

@router.delete('/category/{id}')
def change_name_category(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    category = db.query(DbCategories).filter(DbCategories.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category not exists",
        )
    db.delete(category)
    db.commit()
    return {'message': 'category updated'}

@router.get('/categoris', response_model=List[GetCategory])
def get_categories(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    check_admin(current_user.role)
    categories = db.query(DbCategories).all()
    return categories