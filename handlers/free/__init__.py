from aiogram import Router
from .menu import menuRouter 
from .horoscope import horoscopeRouter

# folder root router
freeRouter: Router = Router()

# connected routers
freeRouter.include_router(horoscopeRouter)
freeRouter.include_router(menuRouter)
