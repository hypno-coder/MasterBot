from aiogram import Router
from .menu import menuRouter 
from .horoscope import horoscopeRouter

freeRouter: Router = Router()

freeRouter.include_router(horoscopeRouter)
freeRouter.include_router(menuRouter)
