from aiogram import Router
from .handlers import horoscopeHandlerRouter 

horoscopeRouter: Router = Router()
horoscopeRouter.include_router(horoscopeHandlerRouter)

