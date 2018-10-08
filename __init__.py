import os
from cudatext import *

FORMSIZEX = 300
FORMSIZEY = 580
COLORLIST = 0xFFFFFF
COLORSEL = 0xE0A0A0

img = image_proc(0, IMAGE_CREATE, value=0)


class Command:

    icon_size = 32
    filter = ''
    files = []
    filedir = ''
    result = ''


    def get_iconset(self, basedir):
    
        dirs = sorted(os.listdir(basedir))
        dirs = [d for d in dirs if '_' in d and 'x' in d]
        res = dlg_menu(MENU_LIST, dirs, caption='Choose icon set')
        if res is not None:
            return os.path.join(basedir, dirs[res])
            
    
    def get_files(self, basedir):
    
        ff = sorted(os.listdir(basedir))
        ff = [os.path.join(basedir, f) for f in ff if f.endswith('.png')]
        #print('files:', ff)
        return ff

    
    def update_filter(self):
        dlg_proc(self.h_dlg, DLG_CTL_PROP_SET, name='filter', prop={'cap': 'Filter: '+self.filter})

        listbox_proc(self.h_list, LISTBOX_DELETE_ALL)

        items = [os.path.basename(f)[:-4] for f in self.files]
        for (i, item) in enumerate(items):
            if not self.filter or self.filter in item:
                listbox_proc(self.h_list, LISTBOX_ADD, index=-1, text=item)

        listbox_proc(self.h_list, LISTBOX_SET_TOP, index=0)
        listbox_proc(self.h_list, LISTBOX_SET_SEL, index=0)


    def callback_keydown(self, id_dlg, id_ctl, data='', info=''):

        #react to text
        if (ord('A') <= id_ctl <= ord('Z')) or \
           (ord('0') <= id_ctl <= ord('9')):
            self.filter += chr(id_ctl).lower()
            self.update_filter()

        #react to BackSp
        if id_ctl==8:
            if self.filter:
                self.filter = self.filter[:-1]
                self.update_filter()

        #react to Enter
        if id_ctl==13:
            index_sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
            item = listbox_proc(self.h_list, LISTBOX_GET_ITEM, index=index_sel)
            if not item: return
            item_text = item[0]

            self.result = os.path.join(self.filedir, item_text+'.png')
            dlg_proc(self.h_dlg, DLG_HIDE)


    def callback_listbox_drawitem(self, id_dlg, id_ctl, data='', info=''):
        global img

        id_canvas = data['canvas']
        index = data['index']
        rect = data['rect']
        index_sel = listbox_proc(self.h_list, LISTBOX_GET_SEL)
        item_text = listbox_proc(self.h_list, LISTBOX_GET_ITEM, index=index)[0]

        if index==index_sel:
            back_color = COLORSEL
        else:
            back_color = COLORLIST

        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=back_color, style=BRUSH_SOLID)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=rect[0], y=rect[1], x2=rect[2], y2=rect[3])

        size = canvas_proc(id_canvas, CANVAS_GET_TEXT_SIZE, text=item_text)
        canvas_proc(id_canvas, CANVAS_TEXT,
            text = item_text,
            x = rect[0] + self.icon_size + 6,
            y = (rect[1]+rect[3]-size[1])//2 )

        image_proc(img, IMAGE_LOAD, value=os.path.join(self.filedir, item_text+'.png'))
        image_proc(img, IMAGE_PAINT_SIZED, value=(id_canvas, rect[0], rect[1], rect[0]+self.icon_size, rect[1]+self.icon_size))


    def init_dlg(self):

        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={'cap':'Choose icon',
          'w':FORMSIZEX,
          'h':FORMSIZEY,
          'on_key_down': self.callback_keydown,
          'keypreview': True
          })

        n=dlg_proc(h, DLG_CTL_ADD, 'label')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'filter',
            'align': ALIGN_TOP,
            'sp_a': 6,
            'cap': '',
            })

        n=dlg_proc(h, DLG_CTL_ADD, 'listbox_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={'name': 'list1',
            'align': ALIGN_CLIENT,
            'sp_a': 6,
            'on_draw_item': self.callback_listbox_drawitem,
            })

        self.h_list = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        dlg_proc(h, DLG_CTL_FOCUS, index=n)

        listbox_proc(self.h_list, LISTBOX_SET_DRAWN, index=1)

        return h


    def __init__(self):
    
        self.h_dlg = self.init_dlg()


    def dialog(self):

        dir = os.path.join(os.path.dirname(__file__), 'icons')    
        self.filedir = self.get_iconset(dir)
        if not self.filedir: return
        
        s = self.filedir[-2:]
        self.icon_size = int(s)
        listbox_proc(self.h_list, LISTBOX_SET_ITEM_H, index=max(18, self.icon_size))

        self.files = self.get_files(self.filedir)
        if not self.files: return 

        self.filter = ''        
        self.update_filter()
        
        dlg_proc(self.h_dlg, DLG_SHOW_MODAL)
        if self.result:
            print('Result:', self.result)
            return self.result
