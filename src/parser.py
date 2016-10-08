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

import argparse
import datetime
import urllib.request, urllib.error, urllib.parse

import httplib2
import os
import sys


import lp3_parser
import youtube

from oauth2client import tools



def _args():
    parser = argparse.ArgumentParser(parents=[tools.argparser])

    parser.add_argument('--notowanie', type=int, required=True)
    parser.add_argument('--rok', type=int, default=datetime.date.today().year)

    return parser.parse_args()


def main():
    args = _args()
    parse_url = lp3_parser.URL.format(notowanie=args.notowanie, rok=args.rok)
    yt = youtube.get_youtube(args)

    f = urllib.request.urlopen(parse_url)
    parser = lp3_parser.LP3HTMLParser()
    parser.feed(f.read().decode(f.headers.get_content_charset()))
    video_ids = []
    for chl in parser.chart_list:
        if not chl:
            continue
        video = youtube.youtube_search(yt, q=' '.join(chl).strip().replace('\n', ''))
        items = video.get('items', None)
        if items is not None:
            print('{}: {}'.format(' '.join(chl).strip().replace('\n', ''), 
                                  items[0]['snippet']['title']))
            videoId = items[0]['id']['videoId']
            video_ids.append((videoId, items[0]['snippet']['title']))

    print(('Found {} videos'.format(len(video_ids))))
    playlist = youtube.create_playlist(
        yt, 'LP3 - {} ({})'.format(args.notowanie, args.rok),
        'Notowanie {notowanie} ({rok}) listy przebojów Trójki {url}'.format(
            notowanie=args.notowanie, rok=args.rok, url=parse_url))
    if playlist:
        print(('Playlist id: {}'.format(playlist['id'])))
        for video_id, title in video_ids:
            print(('Added {} - {}'.format(video_id, title)))
            youtube.add_video_to_playlist(yt, video_id, playlist['id'])


if __name__ == '__main__':
    main()
