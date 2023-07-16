from aiogram import Router

from .common import commonRouter
from .free import freeRouter
from .paid import paidRouter
from .main_menu import menuRouter 

# folder root router
mainRouter: Router = Router()

# connected routers
mainRouter.include_router(menuRouter)
mainRouter.include_router(paidRouter)
mainRouter.include_router(freeRouter)
mainRouter.include_router(commonRouter)
