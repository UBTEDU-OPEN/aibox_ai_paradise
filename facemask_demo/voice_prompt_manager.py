#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# File      : voice_prompt_manager.py
# Created   : 2020/5/26 3:30 下午
# Author    : jesse (jesse.huang@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# ----
# Description:
#

import os
import pyaudio
import wave
import logging

import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
sys.path.append('..')
from common.utility.configure_string_single import ConfigureStringSingle


class VoicePromptManager(object):

    last_compare_count = int(0) #上次播放音频时的个数
    current_change_count = int(0) #更改的个数

    def __init__(self):
        self.queue = []
        self.playing = False
        self.on = False
        self.thread = None
        # self.set_change_count(1)
        #
        # # 打断播放测试代码
        # s = threading.Timer(1, self.countTest,[2])
        # s.start()

        self._start_play()

    def countTest(self,count):
        self.set_change_count(count)

    def set_change_count(self, count):
        self.current_change_count = count
        # 设置个数的时候触发一次尝试播放
        self.attempt_play()

    def attempt_play(self):
        if not self.on:
            return
        if not self.playing:
            if self.current_change_count > 0:
                # print(self.current_change_count)
                # print(self.last_compare_count)
                if self.current_change_count != self.last_compare_count:
                    self.last_compare_count = self.current_change_count
                    self._start_play()
                # else:
                #     #数目相同，不播放
                #     print('count equals, do not play')
            else:
                # print('no unware count, do not play')
                self.last_compare_count = 0
        else:
            logging.debug('present playing')

    def set_on(self, on=False):
        self.on = on
        if self.thread:
            self.thread.on = on
        # 只需更改开关状态
        if not self.on:
            logging.debug('voice status: off')
            self.current_change_count = self.last_compare_count = 0
        else:
            logging.debug('voice status: on')
            self.attempt_play()

    def stop_play(self):

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.playing = False

    def _play_finished(self):
        logging.debug('play finish')
        self.playing = False
        # if self.on:
        #     if not self.playing:
        #         self.attempt_play()

    def _start_play(self):
        if self.last_compare_count <= 0:
            return

        if self.thread is not None:
            self.thread.wait(20000)

        self.playing = True

        self.thread = VoiceThread(self.on)
        self.thread.play_voice_finished_signal.connect(self._play_finished)
        self.thread.start()
        # self.thread.exec()
        # self.thread.wait(10000)

        # chunk = 512
        # wav_path = os.path.join(os.path.dirname(__file__), "mask.wav")
        # wf = wave.open(wav_path, 'rb')
        # self.audio = pyaudio.PyAudio()
        # self.stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
        #                 channels=wf.getnchannels(),
        #                 rate=wf.getframerate(),
        #                 output=True)
        # data = wf.readframes(chunk)
        # print('start play')
        # # 开光状态和数据流同时满足才播放
        # while len(data) > 0 and self.on:
        #     self.stream.write(data)
        #     data = wf.readframes(chunk)
        # else:
        #     self.stream.stop_stream()
        #     self.stream.close()
        #     self.audio.terminate()
        #
        #     self._play_finished()

class VoiceModel(object):

    def __init__(self, timestamp = 0, parent = None, filePath = ''):
        self.timestamp = timestamp
        self.parent = parent
        self.filePath = filePath

from PyQt5.QtCore import pyqtSignal, QThread

class VoiceThread(QThread):
    play_voice_finished_signal = pyqtSignal()

    def __init__(self, on):
        super(VoiceThread, self).__init__()
        configure_file_path = os.path.dirname(os.path.realpath(__file__)) + "/config/locale"
        self.conf = ConfigureStringSingle(configure_file_path, 'facemask')
        self.on = on

    def run(self):
        chunk = 512
        filename = self.conf.get_value_for_key("k_voice_name") + '.wav'
        wav_path = os.path.join(os.path.dirname(__file__), filename)
        print('------',wav_path)
        wf = wave.open(wav_path, 'rb')
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
                                      channels=wf.getnchannels(),
                                      rate=wf.getframerate(),
                                      output=True)
        data = wf.readframes(chunk)
        logging.debug('start play')
        # 开光状态和数据流同时满足才播放
        while len(data) > 0 and self.on:
            self.stream.write(data)
            data = wf.readframes(chunk)
        else:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            self.play_voice_finished_signal.emit()


# if __name__ == '__main__':
#     app = qapp()
#

#
#     currentPath = QDir.currentPath()
#     duanPath = currentPath + '/duanwujie.mp3'
#     childPath = currentPath + '/child.mp3'
#
#     manager.add_task(VoiceModel(0, None, duanPath))
#     manager.add_task(VoiceModel(110, None, ''))
#
#     now = int(time.time())
#     manager.add_task(VoiceModel(now, None, duanPath))
#     manager.add_task(VoiceModel(now, None, duanPath))
#     manager.add_task(VoiceModel(now + 2, None, childPath))
#     manager.set_on(False)
#     manager.add_task(VoiceModel(now + 10, None, childPath))
#     sys.exit(app.exec_())



# manager = VoicePromptManager()
