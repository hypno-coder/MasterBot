from aiogram import Router
from .handlers import calendarHandlerRouter 

calendarRouter: Router = Router()
calendarRouter.include_router(calendarHandlerRouter)

