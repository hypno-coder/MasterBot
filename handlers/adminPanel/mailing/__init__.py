from aiogram import Router

from .handlers import mailingHandlerRouter

mailingRouter: Router = Router()
mailingRouter.include_router(mailingHandlerRouter)
