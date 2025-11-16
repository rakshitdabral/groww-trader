import os
import sys
from dotenv import load_dotenv
load_dotenv()

GROWW_API_KEY = os.getenv("GROWW_API_KEY")
GROWW_API_SECRET = os.getenv("GROWW_API_SECRET")
