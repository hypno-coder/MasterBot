from aiogram import Router

from .menu import adminMenuRouter
from .admin_calculate import adminCalcRouter
from .mailing import mailingRouter
from .lock_control import lockControlRouter

# folder root router
adminRouter: Router = Router()

# connected routers
adminRouter.include_router(adminMenuRouter)
adminRouter.include_router(adminCalcRouter)
adminRouter.include_router(lockControlRouter)
adminRouter.include_router(mailingRouter)
