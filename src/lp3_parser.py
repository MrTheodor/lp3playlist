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

import html.parser


URL='http://lp3.polskieradio.pl/notowania/?rok={rok}&numer={notowanie}'


class LP3HTMLParser(html.parser.HTMLParser, object):
    def __init__(self):
        self.current_artist = None
        self.in_right_box = False
        self.in_boxTrack = False
        self.in_a = False
        self.chart_list = []
        self.tmp_element = []
        self.div_idstack = []
        super(LP3HTMLParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        d_attrs = dict(attrs)
        if tag == 'div':
            self.div_idstack.insert(0, d_attrs)
            if d_attrs.get('id') == 'contRightCont':
                self.in_right_box = True
            elif self.in_right_box and d_attrs.get('class') == 'BoxTrack':
                self.in_boxTrack = True
        if tag == 'a' and self.in_boxTrack:
            self.in_a = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_idstack:
                d = self.div_idstack.pop(0)
            if d.get('class') == 'BoxTrack':
                self.in_boxTrack = False
                self.chart_list.append(self.tmp_element[:])
                self.tmp_element = []
            elif d.get('id') == 'contRightCont':
                self.in_right_box = False
        if tag == 'a' and self.in_a:
            self.in_a = False

    def handle_data(self, data):
        if self.in_a and self.in_right_box and self.in_boxTrack:
            self.tmp_element.append(data.strip().replace('\n', ''))
