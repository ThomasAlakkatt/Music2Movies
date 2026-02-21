import os
from dotenv import load_dotenv
import requests


load_dotenv()
myBearerToken = os.getenv('TMDB_API_READ_ACCESS_TOKEN')

# Movie search by genre API:

# https://developer.themoviedb.org/reference/discover-movie