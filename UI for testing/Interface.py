from PyQt5 import QtCore, QtWidgets
import os
from PyQt5.QtCore import Qt
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor


import Db


class Test:
    def __init__(self):
        self.x = 'Test'
            
        
    def search_finder(self, query):  
        return Db.get_numbers(query)
    
    
class ScrollLabel(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
        self.setFixedSize(700, 550)
        self.setWidgetResizable(True)
        content = QtWidgets.QWidget(self)
        self.setWidget(content)
        lay = QtWidgets.QVBoxLayout(content)
        self.label = QtWidgets.QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setFont(QtGui.QFont('Menlo', 18))   
        lay.addWidget(self.label)
 
    
    def setText(self, text):
        self.label.setText(text)
        
    
class AnotherWindow(QtWidgets.QWidget):
    def __init__(self, text):
        super().__init__()
        self.scroll = ScrollLabel(self)
        self.scroll.setGeometry(10, 10, 800, 650)
        output = Db.get_acts(text)
        self.scroll.setText(output)
        
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Precedent")
        self.resize(1366, 768)
        self.folder = None
        self.set_UI(self)
        self.show()
        
        
    def set_UI(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.textB = QtWidgets.QTextBrowser(self.centralwidget)
        self.textB.setGeometry(QtCore.QRect(700, 500, 600, 50))
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(500, 20, 800, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Введите требование или номер дела...")
        
        self.label0 = QtWidgets.QLabel(self.centralwidget)
        self.label0.setGeometry(QtCore.QRect(50, 10, 390, 70))
        self.label0.setObjectName("label0")
        self.label0.setText("ПРЕЦЕДЕНТ")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(700, 80, 270, 30))
        self.label.setObjectName("label")
        self.label.setText("Похожие дела:")
        
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        QToolTip.setFont(QFont('Menlo', 20))
        your_text = 'Подсказка'
        self.listWidget.setToolTip(your_text)
        self.listWidget.setGeometry(QtCore.QRect(700, 120, 600, 350))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.SelectionMode()
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        #Categories
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(50, 120, 600, 550))
        self.treeView.setHeaderHidden(True)
        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()
        
        s1 = Db.get_cat_1()
        items1 = []
        for item1 in s1:
            i1 = StandardItem(item1, 18, set_bold = False)
            
            s2 = Db.get_cat_2(item1)
            items2 = []
            for item2 in s2:
                i2 = StandardItem(item2, 12)
                
                s3 = Db.get_cat_3(item2)
                items3 = []
                for item3 in s3:
                    i3 = StandardItem(item3, 10)
                    items3.append(i3)
                i2.appendRows(items3)
                
                items2.append(i2)
            i1.appendRows(items2)
            items1.append(i1)
            
        self.rootNode.appendRows(items1)

        self.treeView.setModel(self.treeModel)
        self.treeView.expandAll()
        self.treeView.doubleClicked.connect(self.getValue)

        
        #self.handler()
        self.lineEdit.editingFinished.connect(self.handler)
        
        #self.handler2()
        self.listWidget.itemClicked.connect(self.handler2) 
          
        
    def getValue(self, val):
        test = Test()
        t = val.data()
        l = test.search_finder(t)
        self.listWidget.clear()
        self.listWidget.addItems(l)
        
        
    def handler(self):
        test = Test()
        t = str(self.lineEdit.text())
        l = test.search_finder(t)
        self.listWidget.clear()
        self.listWidget.addItems(l)
          
        
    def handler2(self, item):
        self.show_new_window(item.text())
        solution = Db.get_solution(item.text())
        self.textB.setText(solution)
        
        
    def show_new_window(self, text):
        self.w = AnotherWindow(text)
        self.w.show()


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Menlo', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setFont(fnt)
        self.setText(txt)


if __name__ == "__main__":
    Db.start()
    app = QtWidgets.QApplication(sys.argv)
    style = """
        QWidget{
            background-color: #ffffff;    
        }
        QTextBrowser{
            font-size: 18px;
            font-family: Menlo;
            border-color: #aec2ea;
            border-width: 2px;
            border-style: solid;
            border-radius: 8px;
        }
        QLineEdit{
            font-size: 18px;
            font-family: Menlo; 
            border-color: #aec2ea;
            border-width: 2px;
            border-style: solid;
            border-radius: 8px;
        }
        QLabel#label0{
            font-size: 70px;
            font-family: Menlo; 
            color: #aec2ea; 
        }
        QLabel#label{
            font-size: 24px;
            font-family: Menlo; 
        }
        QListWidget{
            font-size: 18px;
            font-family: Menlo; 
            background-color: #aec2ea; 
            border-color: #aec2ea;
            border-width: 2px;
            border-style: solid;
            border-radius: 8px;
        }
        QScrollArea > QWidget{
            background-color: black;
        }
        QTreeView{
            border-color: #aec2ea;
            border-width: 2px;
            border-style: solid;
            border-radius: 8px;
        }
    """
    app.setStyleSheet(style)
    window = MainWindow()
    #sys.exit(app.exec_())