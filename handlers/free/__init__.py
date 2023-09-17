from aiogram import Router

from .menu import menuRouter 
from .horoscope import horoscopeRouter
from .advisor import advisorRouter

freeRouter: Router = Router()

freeRouter.include_router(horoscopeRouter)
freeRouter.include_router(advisorRouter)
freeRouter.include_router(menuRouter)
