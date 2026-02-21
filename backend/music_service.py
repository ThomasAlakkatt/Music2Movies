# OS allows access to my environmental variables
import os
# re is the RegEx library for RegEx operations
import re
# dotenv loads the .env file, i do import load_dotenv from here because it makes it easier to do something like
# just load_dotenv() as opposed to dotenv.load_dotenv(). Just makes the code cleaner!
from dotenv import load_dotenv
import discogs_client
from discogs_client.exceptions import DiscogsAPIError, AuthorizationError

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

# All functions that make a call using client.ACTION, we will need to wrap it in a try except block for an exception handling catch all

# year is an int, styles is a list, artists is a list, country is a string (Can be None, Worldwide, or specific), genres is a list.

# Adding a seperate function to parse out the 'artists' part of the response
# The only HTTP response I want from this is a 200 OK, the rest of them (there are 8 others) are different use cases that I should
# address 


def release_details(release_id_number):
    try:
        response = client.release(release_id_number)
        release_details_dict = {
            "year": response.year,
            "styles": response.styles,
            "artists": parse_artists(response.artists),
            "country": response.country,
            "genres": response.genres
        }
        return release_details_dict
    except DiscogsAPIError as e:
        print(f"Discogs API Error {e}")
        return None
    except AuthorizationError as e:
        print(f"Authorization Error {e}")
        return None
    except Exception as e:
        print(f"Internal Error {e}")
        return None

# This function parses the artists list that is returned from the client, then returns the parsed list of one or more strings,
# I dont think I need artist ID at this point, maybe down the line for reference info, and pictures of the artist which would be cool
def parse_artists(artists):
    # iterate over the list, this goes through each artist
    # make a dict with artist id as a key and name as value, we can add the pictures in 
    # later when we wanna display, when we do this we can change format
    artist_dict = {}
    for artist_entry in artists:
        clean_name = clean_artist_name(artist_entry.name)
        artist_dict[artist_entry.id] = {
            "name": clean_name
        }
    return artist_dict


# need to set-up search here, limit it to the first 15 results for the time being, we can expand if needed
# dont hard code a number, leave it as a variable so that we can adjust it if needed

# This search function (as it is now) behaves like the "Advanced Search" feature in Discogs
def search_releases(artist_name, releaseTitle, number_of_results=10, page_number=1, music_type="master"):

    # The type here is set to "Master". This is useful because it combines all the different releases of a song or an album into one,
    # consolidated item. This way, we won't be displaying duplicate items fto the user. 

    # this will be user input, so make sure to consider empty name and title variables, and to cut out any whitespaces from them too
    # if artist name OR release title is empty:

    # strips both strings of leading and trailing white spaces
    # remember that python strings are immutable, hence why we need to reassign instead of simply having artist_name.strip() for example
    artist_name = artist_name.strip()
    releaseTitle = releaseTitle.strip()

    # This checks for empty strings, None values, and White-space only values (after strip)
    if not artist_name or not releaseTitle:
        return "One or more fields are blank"

    search_results = client.search(
        artist=artist_name,
        release_title=releaseTitle,
        per_page=number_of_results,
        page=page_number,
        type=music_type
        )
    
    if not search_results:
        print("No results, strange...")
        return None


    # We will be returning the output from the search API as a list of dictionaries, with the entries containing the information
    # for each search result

    # This is the list that will store the dictionaries
    search_list = []


    for release in search_results:
        search_dict = {}
        search_dict["id"] = release.id
        search_dict["title"] = release.title
        search_dict["year"] = release.year
        search_dict["artists"] = [clean_name(artist.name) for artist in release.main_release.artists]
        search_dict["labels"] = [clean_name(label.name) for label in release.main_release.labels]
        search_list.append(search_dict)




    





# check default number of returns without specifying
# check if we need to go page 0 (0 index or if one is correct)
# check if we even need to specify the page number (albeit it wouldnt hurt just to leave it)




# The regex function is used to clean up the artist and label name(s). This is because of how Discogs displays these
def clean_name(media_name):
    # \s* = optional whitespace
    # \(\d+\) = parentheses with digits
    # $ = at end of string
    media_name = re.sub(r'\s*\(\d+\)$', '', media_name)
    return media_name


                
        


search_artist = input("First, enter the name of an artist: ")
search_music = input("Now, enter the name of a song or album: ")

search_releases(search_artist, search_music)




