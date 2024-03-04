from aiogram import Router

from .handlers import destinyCardHandlerRouter
from .menu import destinyCardMenuRouter

destinyCardRouter: Router = Router()
destinyCardRouter.include_router(destinyCardMenuRouter)
destinyCardRouter.include_router(destinyCardHandlerRouter)
