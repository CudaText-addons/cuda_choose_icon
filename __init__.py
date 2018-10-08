import os
from cudatext import *
from .dlg_choose_icon import DialogChooseIcon

class Command:

    def __init__(self):
    
        self.dlg = DialogChooseIcon()

    def dialog(self):

        dir = os.path.join(os.path.dirname(__file__), 'icons')
        res = self.dlg.choose_icon(dir)
        if res:
            print('Chosen icon:', res)
