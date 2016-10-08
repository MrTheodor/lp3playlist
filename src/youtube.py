#!/usr/bin/env python
"""
Copyright (C) 2016 Jakub Krajniak <jkrajniak@gmail.com>

This file is distributed under free software licence:
you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
URL='http://lp3.polskieradio.pl/notowania/?rok={rok}&numer={notowanie}'

def get_youtube(flags):
    CLIENT_SECRETS_FILE = "client_secrets.json"
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

        %s

        with information from the Developers Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    CLIENT_SECRETS_FILE))

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                    message=MISSING_CLIENT_SECRETS_MESSAGE,
                                    scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION, 
                 http=credentials.authorize(httplib2.Http()))


def create_playlist(youtube, name, description):
    playlists_insert_response = youtube.playlists().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=name,
                description=description
            ),
            status=dict(
                privacyStatus="public"
            )
        )
    ).execute()

    print("New playlist id: %s" % playlists_insert_response["id"])
    return playlists_insert_response


def add_video_to_playlist(youtube, videoID, playlistID):
    add_video_request=youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
                'playlistId': playlistID, 
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': videoID
                }
            #'position': 0
        }}
    ).execute()
    return add_video_request


def youtube_search(youtube, q, max_results=1):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=q + ' official',
        part="id,snippet",
        maxResults=1,
        type='video',
    ).execute()
    return search_response
