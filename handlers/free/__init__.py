from aiogram import Router
from .menu import menuRouter 
from .sonnik import sonnikRouter

# folder root router
freeRouter: Router = Router()

# connected routers
freeRouter.include_router(menuRouter)
freeRouter.include_router(sonnikRouter)
