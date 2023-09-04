from aiogram import Router
from .menu import codeMenuRouter
from .handlers import codeHandlerRouter 

codeRouter: Router = Router()
codeRouter.include_router(codeMenuRouter)
codeRouter.include_router(codeHandlerRouter)

