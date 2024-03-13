from aiogram import Router

from .menu import adminCalcMenuRouter


adminCalcRouter: Router = Router()
adminCalcRouter.include_router(adminCalcMenuRouter)
