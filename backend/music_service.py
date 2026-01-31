# OS allows access to my environmental variables
import os

# dotenv loads the .env file, i do import load_dotenv from here because it makes it easier to do something like
# just load_dotenv() as opposed to dotenv.load_dotenv(). Just makes the code cleaner!
from dotenv import load_dotenv
import discogs_client

# Because of how Discogs API is set-up, I don't need to use the 'requests' library/package here


# Loads the env file in
load_dotenv()

# These two lines load my private, unique user token and user agent into variables
my_user_token = os.getenv('DISCOGS_API_KEY')
my_user_agent = os.getenv('DISCOGS_USER_AGENT')

# This is an object authenticated with my user agent and token that allows me to make calls to the Discogs API!
d = discogs_client.Client(user_agent=my_user_agent, user_token=my_user_token)

