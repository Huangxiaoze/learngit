import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout
#import ReceiptWindows
import receiptwindow
#import table1
import Printer
#import froms
import kucundan
import CommodityData
"""
其他的窗口不应该有show
"""

class Demo(QTabWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.commodity = CommodityData.Commodity()
        self.resize(1000,1000)
        #self.setGeometry(200,200,1000,700)
        #self.tab1 = ReceiptWindows.MyWindow()
        self.tab2 = receiptwindow.MyWindow(self.commodity)
        self.tab3 = kucundan.MyWindow(self.commodity)
        #self.tab4 = table1.TableSheet()
        #self.tab5 = Printer.MyPrinter()
        #self.tab6 = froms.Form()
        self.addTab(self.tab2, '收据')
        #self.addTab(self.tab4,"Tab")
        #self.addTab(self.tab5,"打印机")
        self.addTab(self.tab3, QIcon("n.jpg"), "库存单")
        #self.addTab(self.tab6,"年度月度报表")
        #self.addTab(self.tab1, '收据')  # 3
        self.currentChanged.connect(lambda: print(self.currentIndex()))  # 4
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())