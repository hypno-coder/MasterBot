from aiogram import Router
from .menu import menuRouter
from .jantra import jantraRouter
from .code import codeRouter
from .calendar import calendarRouter

# folder root router
paidRouter: Router = Router()

# connected routers
paidRouter.include_router(menuRouter)
paidRouter.include_router(jantraRouter)
paidRouter.include_router(codeRouter)
paidRouter.include_router(calendarRouter)
