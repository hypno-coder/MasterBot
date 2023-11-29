from aiogram import Router
from .handlers import sonnikHandlerRouter 

sonnikRouter: Router = Router()
sonnikRouter.include_router(sonnikHandlerRouter)

