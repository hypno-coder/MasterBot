from aiogram import Router
from .handlers import handlersRouter 

# folder root router
commonRouter: Router = Router()

# connected routers
commonRouter.include_router(handlersRouter)
