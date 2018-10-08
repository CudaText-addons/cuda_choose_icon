import os
from cudatext import *
from .dialog_choose_icon import DlgChooseIcon

class Command:

    def __init__(self):
    
        self.dlg = DlgChooseIcon()

    def dialog(self):

        dir = os.path.join(os.path.dirname(__file__), 'icons')
        res = self.dlg.choose_icon(dir)
        if res:
            print('Chosen icon:', res)
