from aiogram import Router
from .handlers import sbornikHandlerRouter

sbornikRouter: Router = Router()
sbornikRouter.include_router(sbornikHandlerRouter)
