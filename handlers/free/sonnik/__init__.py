from aiogram import Router
from .handlers import sonnikHandlerRouter 
from .menu import sonnikMenuRouter

sonnikRouter: Router = Router()
sonnikRouter.include_router(sonnikMenuRouter)
sonnikRouter.include_router(sonnikHandlerRouter)

