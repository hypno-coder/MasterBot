from aiogram import Router
from .handlers import codeHandlerRouter 

codeRouter: Router = Router()
codeRouter.include_router(codeHandlerRouter)

