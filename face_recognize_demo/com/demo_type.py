import threading
from enum import Enum


class Type(Enum):
    track_demo_item = 1
    face_demo_item = 2

class DemoType(object):
    _instance_lock = threading.Lock()
    _init_flag = False

    def __init__(self, demo_type=Type.track_demo_item):
        if DemoType._init_flag == False:

            self.type_item = demo_type

            DemoType._init_flag = True

    def __new__(cls, *args, **kwargs):
        if not hasattr(DemoType, "_instance"):
            with DemoType._instance_lock:
                if not hasattr(DemoType, "_instance"):
                    DemoType._instance = object.__new__(cls)

        return DemoType._instance