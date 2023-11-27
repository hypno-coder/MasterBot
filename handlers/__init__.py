from aiogram import Router

from .adminPanel import adminRouter
from .common import commonRouter
from .paid import paidRouter
from .free import freeRouter
from .main_menu import mainMenuRouter

# folder root router
mainRouter: Router = Router()

# connected routers
mainRouter.include_router(mainMenuRouter)
mainRouter.include_router(freeRouter)
mainRouter.include_router(paidRouter)
mainRouter.include_router(commonRouter)
mainRouter.include_router(adminRouter)
