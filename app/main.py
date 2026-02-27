from contextlib import asynccontextmanager

import dotenv
from fastapi import FastAPI
from app.routers import router_list
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
    
dotenv.load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LeetCode Agent Backend is starting up 🚀")
    
    yield  # The application runs here and handles requests

    # Code after the 'yield' is run during application shutdown
    logger.info("LeetCode Agent Backend is shutting down 🛑")
    # Example: await app.state.db_connection.disconnect()

app = FastAPI(lifespan=lifespan)

# Allow CORS for local dev/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in router_list:
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "LeetCode Agent Backend is running 🚀"}