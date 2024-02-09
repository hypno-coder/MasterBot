from aiogram import Router
from .handlers import lockСontrolHandlerRouter 
from .menu import lockControlMenuRouter

lockControlRouter: Router = Router()
lockControlRouter.include_router(lockControlMenuRouter)
lockControlRouter.include_router(lockСontrolHandlerRouter)

