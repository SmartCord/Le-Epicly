from discord.ext import commands
from tools import utils, config
from bs4 import BeautifulSoup as bsoup
from tools.bot_tools import db, reddit
import paginator
from pathlib import Path
import random, requests, asyncio, discord, time, ast, io, traceback, textwrap, aiohttp, uuid
from io import BytesIO
from contextlib import redirect_stdout
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from tools.utils import color, prefix, usage, error, success, footer, botError
from tools.bot_utils import pointless, Counters, giveAchievement, pointlessRaw
