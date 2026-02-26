import requests
import pandas as pd


class Genius:
    """Client for interacting with the Genius API."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.genius.com"


    def get_artist(self, search_term):
        """
        Return a dictionary containing artist information
        from the Genius API.
        """
        # Search for the artist name
        search_url = f"{self.base_url}/search"
        search_response = requests.get(
            search_url,
            headers=self.headers,
            params={"q": search_term},
        )

        search_data = search_response.json()

        # Get the artist ID from the first result
        artist_id = (
            search_data["response"]["hits"][0]
            ["result"]["primary_artist"]["id"]
        )

        # Use the artist ID to get artist info
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(
            artist_url,
            headers=self.headers,
        )

        return artist_response.json()

    def get_artists(self, search_terms):
        """
        Return a DataFrame of artist information for a list
        of search terms.
        """
        results = []

        for term in search_terms:
            artist_json = self.get_artist(term)
            artist_data = artist_json["response"]["artist"]

            row = {
                "search_term": term,
                "artist_name": artist_data.get("name"),
                "artist_id": artist_data.get("id"),
                "followers_count": artist_data.get("followers_count"),
            }

            results.append(row)

        return pd.DataFrame(results)