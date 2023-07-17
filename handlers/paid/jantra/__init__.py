from aiogram import Router
from .menu import jantraMenuRouter 

jantraRouter: Router = Router()
jantraRouter.include_router(jantraMenuRouter)

