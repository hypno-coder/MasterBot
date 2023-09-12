from aiogram import Router

from .common import commonRouter
from .paid import paidRouter
from .free import freeRouter

# folder root router
mainRouter: Router = Router()

# connected routers
mainRouter.include_router(freeRouter)
mainRouter.include_router(commonRouter)
