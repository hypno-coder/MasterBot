from aiogram import Router

from .common import commonRouter
from .paid import paidRouter

# folder root router
mainRouter: Router = Router()

# connected routers
mainRouter.include_router(paidRouter)
mainRouter.include_router(commonRouter)
