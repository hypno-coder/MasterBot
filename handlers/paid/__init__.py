from aiogram import Router

from .calendar import calendarRouter
from .code import codeRouter
from .destiny_card import destinyCardRouter
from .jantra import jantraRouter
from .menu import menuRouter

paidRouter: Router = Router()

paidRouter.include_router(menuRouter)
paidRouter.include_router(jantraRouter)
paidRouter.include_router(codeRouter)
paidRouter.include_router(calendarRouter)
paidRouter.include_router(destinyCardRouter)
