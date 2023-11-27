from aiogram import Router

from .menu import adminMenuRouter
from .mailing import mailingRouter

# folder root router
adminRouter: Router = Router()

# connected routers
adminRouter.include_router(adminMenuRouter)
adminRouter.include_router(mailingRouter)
