from fastapi import FastAPI

from fast_zero.routers import auth, health, user

app = FastAPI(
    title='🚀 FAST API',
    version='0.1.0',
    description='✨ API FOR LEARNING FASTAPI ✨',
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)
