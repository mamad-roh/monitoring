from database import database
from fastapi import FastAPI
from routers import user, authentication, contact, server

app = FastAPI()

# ساخت تیبل های دیتابیس با توجه به کلاس های مدل
database.Base.metadata.create_all(bind=database.engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(contact.router)
app.include_router(server.router)
