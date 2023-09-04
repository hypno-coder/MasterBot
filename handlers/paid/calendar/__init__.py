from aiogram import Router
from .menu import calendarMenuRouter
from .handlers import calendarHandlerRouter 

calendarRouter: Router = Router()
calendarRouter.include_router(calendarMenuRouter)
calendarRouter.include_router(calendarHandlerRouter)

