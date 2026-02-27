from app.routers import auth

# List of all routers to be included by the FastAPI app
router_list = [
    auth.router,
]
