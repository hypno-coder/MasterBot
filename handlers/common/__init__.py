from aiogram import Router

from .handlers import handlersRouter

commonRouter: Router = Router()

commonRouter.include_router(handlersRouter)
