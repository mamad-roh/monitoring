from database import database
from fastapi import FastAPI
from routers import (
    user,
    authentication,
    contact,
    server,
    manage_server,
    media,
    web_hook,
    media_manage
)

app = FastAPI()

# ساخت تیبل های دیتابیس با توجه به کلاس های مدل
database.Base.metadata.create_all(bind=database.engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(contact.router)
app.include_router(server.router)
app.include_router(media.router)
app.include_router(manage_server.router)
app.include_router(media_manage.router)
app.include_router(web_hook.router)
