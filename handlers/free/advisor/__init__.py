from aiogram import Router
from .menu import advisorMenuRouter 
from .handlers import advisorHandlerRouter

advisorRouter: Router = Router()
advisorRouter.include_router(advisorMenuRouter)
advisorRouter.include_router(advisorHandlerRouter)

