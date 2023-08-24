from aiogram import Router
from .menu import jantraMenuRouter 
from .handlers import jantraHandlerRouter

jantraRouter: Router = Router()
jantraRouter.include_router(jantraMenuRouter)
jantraRouter.include_router(jantraHandlerRouter)

