# OS allows access to my environmental variables
import os
import re
# dotenv loads the .env file, i do import load_dotenv from here because it makes it easier to do something like
# just load_dotenv() as opposed to dotenv.load_dotenv(). Just makes the code cleaner!
from dotenv import load_dotenv
import discogs_client

# Because of how Discogs API is set-up, I don't need to use the 'requests' library/package here

# Just for testing, remove this in the final version 
from music_service_testdata import release_data

# Loads the env file in
load_dotenv()

# These two lines load my private, unique user token and user agent into variables
my_user_token = os.getenv('DISCOGS_API_KEY')
my_user_agent = os.getenv('DISCOGS_USER_AGENT')

# This is an object authenticated with my user agent and token that allows me to make calls to the Discogs API!
client = discogs_client.Client(user_agent=my_user_agent, user_token=my_user_token)

# year is an int, styles is a list, artists is a list, country is a string (Can be None, Worldwide, or specific), genres is a list.

# Adding a seperate function to parse out the 'artists' part of the response
# The only HTTP response I want from this is a 200 OK, the rest of them (there are 8 others) are different use cases that I should
# address 
def release_details(release_id_number):
    response = client.release(release_id_number)
    # Call another function that can parse out the artists portion
    release_details_dict = {
        "year": response.year,
        "styles": response.styles,
        # Figure out a way to scrape the artist ID, and then the name from the response artists. 
        "artists": parse_artists(response.artists),
        "country": response.country,
        "genres": response.genres,
    }
    return release_details_dict

# This function parses the artists list that is returned from the client, then returns the parsed list of one or more strings,
# I dont think I need artist ID at this point, maybe down the line for reference info, and pictures of the artist which would be cool

# Artists is a list, the format is roughly the same for each entry with some exceptions (Future shows up as Future (4)??)
# Another thing to consider when parsing is how ' may be apart of an artist's name, so it may not be reliable to parse looking at just
# what is contained in the ''s

# another alternative is to get just the artist ID, then make a separate API call to artists API to get a better format for artist names
# provided by Discogs itself (this comes in the form of another list of string titled "variations", albeit we can use the first 1 or 2)

def parse_artists(artists):
    # iterate over the list, this goes through each artist
    # make a dict with artist id as a key and name as value, we can add the pictures in 
    # later when we wanna display, when we do this we can change format
    artist_dict = {}
    for artist_entry in artists:
        # \s* = optional whitespace
        # \(\d+\) = parentheses with digits
        # $ = at end of string
        clean_name = re.sub(r'\s*\(\d+\)$', '', artist_entry.name)
        artist_dict[artist_entry.id] = {
            "name": clean_name
        }
    return artist_dict




                
        



