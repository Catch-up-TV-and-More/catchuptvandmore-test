# -*- coding: utf-8 -*-

import subprocess

class Player:
    def __init__(self, url):
        self.url = url

    def play(self):
        #  We start mpv with the video
        p = subprocess.Popen(['mpv', self.url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output, err) = p.communicate()
        retval = p.wait()
        print('MPV_STDOUT: \n' + output.decode('utf-8'))





# if not CONFIG['disable_video_player']:
#     #  We start mpv with the video
#     p = subprocess.Popen(['mpv', runtime.CURRENT_PATH[-1]['video']['url']], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     output = ''

#     if CONFIG['auto_exploration']:
#         # We need to stop the video after some time
#         time.sleep(5)
#         p.send_signal(signal.SIGINT)

#         (output, err) = p.communicate()
#         retval = p.wait()  # Maybe not needed?

#     else:
#         # The user need to manually close mpv
#         (output, err) = p.communicate()
#         retval = p.wait()

#     MPV_STDOUT = output.decode('utf-8')
#     # print('MPV_STDOUT: \n' + MPV_STDOUT)

#     if 'Exiting... (Quit)' not in MPV_STDOUT:
#         print(WARNING + ' This video does not seem to work (see log above) ' + WARNING)
#         print('')

#         runtime.ALL_REPORTED_ERROR.append({
#             'type': 'Video',
#             'path': current_path_pp(runtime.CURRENT_PATH),
#             'route': bridge.TRIGGER_ERROR_ROUTE,
#             'params': bridge.TRIGGER_ERROR_PARAMS
#         })

#         if CONFIG['exit_on_error']:
#             next_item = -1