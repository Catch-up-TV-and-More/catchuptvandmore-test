# -*- coding: utf-8 -*-

import sys
import mock
from config import *

mock_xbmcvfs = mock.MagicMock()

# Say to Python that the xbmcvfs module is mock_xbmcvfs
sys.modules['xbmcvfs'] = mock_xbmcvfs
