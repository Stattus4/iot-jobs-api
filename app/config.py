# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
