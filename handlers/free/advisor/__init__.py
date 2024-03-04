from aiogram import Router

from .handlers import advisorHandlerRouter
from .menu import advisorMenuRouter

advisorRouter: Router = Router()
advisorRouter.include_router(advisorMenuRouter)
advisorRouter.include_router(advisorHandlerRouter)
