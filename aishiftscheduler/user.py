# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/routers/16_user.ipynb.

# %% auto 0
__all__ = ['create_user', 'get_user']

# %% ../nbs/routers/16_user.ipynb 7
# from pydantic import BaseModel, EmailStr
# from datetime import datetime

# %% ../nbs/routers/16_user.ipynb 8
## users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=sch.UserOut)
def create_user(user: sch.UserCreate, db: Session=Depends(get_db)):

    # has the password - user.password
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = utl.hash(user.password)
    user.password = hashed_password

    new_user = dbm.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# %% ../nbs/routers/16_user.ipynb 9
@app.get("/users/{id}", response_model=sch.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(dbm.User).filter(dbm.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")    
    return user
