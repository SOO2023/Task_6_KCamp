from fastapi import FastAPI
from database import Base, engine
from routers import blog, auth, user, task, admin, e_comm


app = FastAPI()

Base.metadata.create_all(bind=engine)

routers = [
    blog.router,
    auth.router,
    user.router,
    task.router,
    admin.router,
    e_comm.router,
]
for router in routers:
    app.include_router(router)
