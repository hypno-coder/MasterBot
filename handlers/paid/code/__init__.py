from aiogram import Router

from .handlers import codeHandlerRouter
from .menu import codeMenuRouter

codeRouter: Router = Router()
codeRouter.include_router(codeMenuRouter)
codeRouter.include_router(codeHandlerRouter)
