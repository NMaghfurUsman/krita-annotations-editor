import krita
import os
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6 import uic
    from PyQt6.QtWidgets import *
except:
    from PyQt5 import uic
    from PyQt5.QtWidgets import *

from krita import *

class annotations_editor(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Annotations Editor")
        self.ui = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),"annotations_editor.ui"))
        
        k = Krita.instance()
        self.ui.writeBtn.setIcon(k.icon('document-export'))
        self.ui.readBtn.setIcon(k.icon('document-import'))
        self.ui.delBtn.setIcon(k.icon('list-remove'))
        self.ui.addBtn.setIcon(k.icon('list-add'))
        self.ui.openBtn.setIcon(k.icon('system-run'))
        self.setWidget(self.ui)

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("annotations_editor", DockWidgetFactoryBase.DockPosition.DockRight, annotations_editor)) 
