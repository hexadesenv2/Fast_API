import asyncio
import sys

from fastapi import FastAPI

from fast_zero.routers import auth, health, todos, user

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title='🚀 FAST API',
    version='0.1.0',
    description='✨ API FOR LEARNING FASTAPI ✨',
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todos.router)
