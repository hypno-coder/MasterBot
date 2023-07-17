from aiogram import Router
from .menu import menuRouter
from .jantra import jantraRouter

# folder root router
paidRouter: Router = Router()

# connected routers
paidRouter.include_router(menuRouter)
paidRouter.include_router(jantraRouter)
