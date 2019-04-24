# -*- coding: utf-8 -*-

import sys
import mock
import subprocess


class Fake_Video_Info(object):
    def __init__(self, url, quality=1, resolve_redirects=False):
        print('[FakeYoutbeDl] Sent command: youtube-dl --get-url {}'.format(url))
        p = subprocess.Popen(['youtube-dl', '--get-url', url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output, err) = p.communicate()
        retval = p.wait()
        output = output.decode('utf-8').split('\n')[0]
        print('[FakeYoutbeDl] Video URL?: {}'.format(output))
        self._stream_url = output
        self.sourceName = 'FAKE'
        if 'dailymotion' in output:
            self.sourceName = 'dailymotion'


    def streamURL(self):
        return self._stream_url

    def hasMultipleStreams(self):
        return False


mock_youtube_dl = mock.MagicMock()
mock_youtube_dl.getVideoInfo.side_effect = Fake_Video_Info

# Say to Python that the YDStreamExtractor module is mock_youtube_dl
sys.modules['YDStreamExtractor'] = mock_youtube_dl
