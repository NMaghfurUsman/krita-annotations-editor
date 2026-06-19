import krita
import os
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6 import uic
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
except:
    from PyQt5 import uic
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

from krita import *

class annotations_editor(DockWidget):
    """
    Simple stateless docker for reading out and saving Document annotations.
    """

    annotationsChanged = pyqtSignal()

    @pyqtProperty(Document)
    def document(self):
        return self.view.document()

    @pyqtProperty(View)
    def view(self):
        return self.canvas().view()

    @pyqtSlot()
    def readOutAnnotation(self):
        annotation_type_name : str = self.ui.annotationCB.currentText()
        if annotation_type_name:
            desc : str = self.document.annotationDescription(annotation_type_name)
            anno : str = bytes(self.document.annotation(annotation_type_name)).decode('utf-8')
            self.ui.annotationDescLE.setText(desc)
            self.ui.annotationTE.setPlainText(anno)

    @pyqtSlot()
    def setAnnotation(self):
        annotation_type_name : str = self.ui.annotationCB.currentText()
        if annotation_type_name:
            desc : str = self.ui.annotationDescLE.text()
            anno : str = self.ui.annotationTE.toPlainText()
            self.document.setAnnotation(annotation_type_name, desc, bytes(anno, 'utf-8'))

    @pyqtSlot()
    def deleteAnnotation(self):
        annotation_type_name : str = self.ui.annotationCB.currentText()
        self.document.removeAnnotation(annotation_type_name)

        self.ui.annotationDescLE.clear()    
        self.ui.annotationTE.clear()

        self.annotationsChanged.emit()
        self.ui.annotationCB.currentIndex = 0

    @pyqtSlot()
    def addAnnotation(self):
        new_annotation_type_name : str = self.ui.lineEdit.text()
        self.ui.lineEdit.clear()
        desc : str = self.ui.annotationDescLE.text()
        anno : str = self.ui.annotationTE.toPlainText()
        self.document.setAnnotation(new_annotation_type_name, desc, bytes(anno, 'utf-8'))
        self.annotationsChanged.emit()

        newest_index : int = len(self.document.annotationTypes())-1
        self.ui.annotationCB.setCurrentIndex(newest_index)

    @pyqtSlot()
    def clearForm(self):
        self.ui.annotationDescLE.clear()    
        self.ui.annotationTE.clear()
        self.ui.lineEdit.clear()

    @pyqtSlot()
    def refreshAnnotations(self):
        self.annotationsChanged.emit()
        self.ui.annotationCB.currentIndex = 0

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Annotations Editor")
        self.ui = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),"annotations_editor.ui"))
        
        k = Krita.instance()
        self.ui.writeBtn.setIcon(k.icon('document-export'))
        self.ui.delBtn.setIcon(k.icon('list-remove'))
        self.ui.addBtn.setIcon(k.icon('list-add'))
        self.ui.clearBtn.setIcon(k.icon('edit-clear'))
        self.ui.refreshBtn.setIcon(k.icon('view-refresh'))
        
        self.ui.writeBtn.clicked.connect(self.setAnnotation)
        self.ui.delBtn.clicked.connect(self.deleteAnnotation)
        self.ui.addBtn.clicked.connect(self.addAnnotation)
        self.ui.clearBtn.clicked.connect(self.clearForm)
        self.annotationsChanged.connect(self.updateCB)
        self.ui.annotationCB.currentIndexChanged.connect(self.readOutAnnotation)
        self.ui.refreshBtn.clicked.connect(self.refreshAnnotations)
        
        self.setWidget(self.ui)    

    @pyqtSlot()
    def updateCB(self):
        # anti-pattern, this is NOT how Qt item model classes should be used
        new_model : QStringListModel = QStringListModel(self.document.annotationTypes())
        self.ui.annotationCB.setModel(new_model)

    def canvasChanged(self, canvas):
        self.clearForm()
        if self.view:
            self.updateCB()


Krita.instance().addDockWidgetFactory(DockWidgetFactory("annotations_editor", DockWidgetFactoryBase.DockPosition.DockRight, annotations_editor)) 
