from aiogram import Router

from .handlers import calendarHandlerRouter
from .menu import calendarMenuRouter

calendarRouter: Router = Router()
calendarRouter.include_router(calendarMenuRouter)
calendarRouter.include_router(calendarHandlerRouter)
