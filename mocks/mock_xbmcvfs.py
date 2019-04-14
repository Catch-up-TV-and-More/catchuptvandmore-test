# -*- coding: utf-8 -*-

import sys
import mock

mock_xbmcvfs = mock.MagicMock()

# Say to Python that the xbmcvfs module is mock_xbmcvfs
sys.modules['xbmcvfs'] = mock_xbmcvfs
