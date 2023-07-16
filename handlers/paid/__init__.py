from aiogram import Router
from .menu import menuRouter

# folder root router
paidRouter: Router = Router()

# connected routers
paidRouter.include_router(menuRouter)
