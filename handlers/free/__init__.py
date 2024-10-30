from aiogram import Router

from .menu import menuRouter 
from .horoscope import horoscopeRouter
# from .advisor import advisorRouter
from .sonnik import sonnikRouter

freeRouter: Router = Router()

freeRouter.include_router(horoscopeRouter)
# freeRouter.include_router(advisorRouter)
freeRouter.include_router(menuRouter)
freeRouter.include_router(sonnikRouter)
