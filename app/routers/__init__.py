from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.utilities.flash import get_flashed_messages
from jinja2 import Environment, FileSystemLoader
from app.config import get_settings
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

template_env = Environment(loader=FileSystemLoader(os.path.join(base_dir, "templates")))
template_env.globals['get_flashed_messages'] = get_flashed_messages
templates = Jinja2Templates(env=template_env)
static_files = StaticFiles(directory=os.path.join(base_dir, "static"))

router = APIRouter(tags=["Jinja Based Endpoints"], include_in_schema=get_settings().env.lower() in ["dev","development"])
api_router = APIRouter(tags=["API Endpoints"], prefix="/api")

from . import (index, login, register, admin_home, user_home, users, logout)