import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from .git import clone_btiq_repo
from .endpoint import router as assistant_router

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing btiq repository")
    clone_btiq_repo()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant_router)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    messages: list


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    return r"""
    <html>
        <body>
            <pre>
 __                  __                                     __                                
/\ \      __        /\ \__  __                             /\ \                               
\ \ \____/\_\     __\ \ ,_\/\_\    ___ ___      __         \ \ \____  __  __     __     ____  
 \ \ '__`\/\ \  /'_ `\ \ \/\/\ \ /' __` __`\  /'__`\ _______\ \ '__`\/\ \/\ \  /'_ `\  /',__\ 
  \ \ \L\ \ \ \/\ \L\ \ \ \_\ \ \/\ \/\ \/\ \/\  __//\______\\ \ \L\ \ \ \_\ \/\ \L\ \/\__, `\
   \ \_,__/\ \_\ \____ \ \__\\ \_\ \_\ \_\ \_\ \____\/______/ \ \_,__/\ \____/\ \____ \/\____/
    \/___/  \/_/\/___L\ \/__/ \/_/\/_/\/_/\/_/\/____/          \/___/  \/___/  \/___L\ \/___/ 
                  /\____/                                                        /\____/      
                  \_/__/                                                         \_/__/ 
            </pre>
            <a href="/docs">swagger -></a>
        </body>
    </html>
    """
