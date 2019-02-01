from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget,
                             QVBoxLayout,
                             QTableWidgetItem, QFrame, QLabel, QGridLayout, QPushButton, QAbstractItemView, QLineEdit,
                             QTextEdit, QCheckBox, QRadioButton, QHBoxLayout, QFileDialog)
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import QRect, Qt, QSize, QPoint, QSizeF
import sys
import datetime
from CommodityData import Commodity
class Cell_Set():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
lower_to_upper = {"0":"零","1":"壹","2":"貳","3":"叁","4":"肆","5":"伍","6":"陆","7":"柒","8":"捌","9":"玖"}
class MyWindow(QWidget):
    def __init__(self,commodity):
        super().__init__()
        self.commoditydata = commodity
        self.TableXY()
        self.initui()
        self.SetLineEditLabel()
        self.show()
    def CheckData(self):
        for i in range(7):
            if self.commoditydata.Find(self.lineedits[i][0].text()):
                k = self.commoditydata.getData(self.lineedits[i][0].text())
                for j in range(1,3):
                    self.lineedits[i][j].setText(k[j])


    def checklineedit(self):
        heji =0
        for i in range(7):
            if self.lineedits[i][4].text() and self.lineedits[i][3].text():
                sum =float(self.lineedits[i][4].text())*float(self.lineedits[i][3].text())*100
                s = str(int(sum))
                heji+=sum
                for j in range(1,len(s)+1):
                    self.labels[i][-j].setText(s[-j])
                for j in range(len(s)+1,8):
                    self.labels[i][-j].setText("")
            else:
                for j in range(8):
                    self.labels[i][j].setText("")
        if heji!=0:
            for i in range(8):
                self.hejilabel[i].setText("")
            self.dollarlabel.setText("")
            h = str(int(heji))
            self.dollarlabel.setText(str(heji/100))
            print(h)
            for i in range(1,len(h)+1):
                self.hejilabel[-i].setText(lower_to_upper[h[-i]])
        else:
            for i in range(8):
                self.hejilabel[i].setText("")
            self.dollarlabel.setText("")
    def SetLineEditLabel(self):
        """
        下面实现的功能是在收据里绘制QFrame,目的是当用户在表格中输入时，将内容填入收据
        """
        self.lineedits = [[QLineEdit("",self) for i in range(5)] for j in range(7)]
        for i in range(7):
            for j in range(5):
                self.lineedits[i][j].setGeometry(self.Cell[i+1][j].x,self.Cell[i+1][j].y,self.Cell[i+1][j].width,self.Cell[i+1][j].height)
                self.lineedits[i][j].setStyleSheet("background-color:rgba(0,255,255,0)")#设置背景色和透明度
                self.lineedits[i][j].setFrame(False)
                if j==4 or j==3:
                    self.lineedits[i][j].textChanged.connect(self.checklineedit)
                elif j==0:
                    self.lineedits[i][j].textChanged.connect(self.CheckData)
        self.labels = [[QLabel(self) for i in range(8)] for j in range(7)]
        for i in range(7):
            for j in range(8):
                self.labels[i][j].setGeometry(self.Change_cell[i][j].x,self.Change_cell[i][j].y,self.Change_cell[i][j].width,self.Change_cell[i][j].height)
        self.beizu = QLineEdit(self)
        self.beizu.setGeometry(self.beizhunext.x,self.beizhunext.y,self.beizhunext.width+1,self.beizhunext.height+1)
        self.beizu.setStyleSheet("background-color:transparent")
        self.beizu.setFrame(QFrame.NoFrame)
        self.customerline = QLineEdit(self)
        self.customerline.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.customerline.setFrame(False)
        self.customerline.setGeometry(self.customer.x + 50, self.customer.y - 20, 300, 30)
        today = datetime.date.today()
        timelabel = [QLabel(self) for t in range(3)]
        timelabel[0].setText(str(today.year))
        timelabel[1].setText(str(today.month))
        timelabel[2].setText(str(today.day))
        for i in range(3):
            if i ==0:
                timelabel[i].setGeometry(self.time[i].x - 35, self.time[i].y - 60, 100, 100)
            else:
                timelabel[i].setGeometry(self.time[i].x-20,self.time[i].y-60,100,100)
        self.hejibottom = [QLineEdit(self) for i in range(3)]
        for i in range(3):
            self.hejibottom[i].setStyleSheet("background-color:rgb(0,0,0,0)")
            self.hejibottom[i].setFrame(False)
            if i <2:
                self.hejibottom[i].setGeometry(self.title3_Cell[i].x+50,self.title3_Cell[i].y-20,200,30)
            else:
                self.hejibottom[i].setGeometry(self.title3_Cell[i].x + 70, self.title3_Cell[i].y - 20, 200, 30)
        self.hejilabel = [QLabel(self) for i in range(8)]
        for i in range(8):
            self.hejilabel[i].setGeometry(self.title2_cell[i].x-20,self.title2_cell[i].y-15,20,20)
        self.dollarlabel = QLabel(self)
        self.dollarlabel.setGeometry(self.title2_cell[7].x+60,self.title2_cell[7].y-15,100,20)
    def Transport(self):
        for i in range(7):
            for j in range(5):
                print(self.lineedits[i][j].text())
    def ChoosePrintColor(self):
        self.colorlabel = QLabel(self)  # 定义这个label是为了给收据上色
        #self.beizhucolor = QLabel(self.preview)
        self.colorlabel.setGeometry(0, 0, 900, 550)
        self.colorlabel.setFrameShape(QFrame.Box)
        self.redcheckbutton =QRadioButton("红色(客户)")
        self.whitecheckbutton=QRadioButton("白色(存根)")
        self.yellowcheckbutton=QRadioButton("黄色(会计)")
        self.bluecheckbutton=QRadioButton("蓝色(回单)")
        frame = QFrame(self)
        frame.setGeometry(700,555,120,120)
        self.vlayout = QVBoxLayout(frame)
        self.vlayout.addWidget(self.redcheckbutton)
        self.vlayout.addWidget(self.whitecheckbutton)
        self.vlayout.addWidget(self.yellowcheckbutton)
        self.vlayout.addWidget(self.bluecheckbutton)

        self.vlayout.addStretch(1)
    def initui(self):
        self.setFixedSize(900,800)
        self.setWindowTitle("收据")
        self.printer = QPrinter(QPrinter.HighResolution)
        self.ChoosePrintColor()
        self.printerbutton = QPushButton("打印",self)
        self.printerbutton.setGeometry(200,600,50,50)
        self.printerbutton.clicked.connect(self.Print)
        #line.setFrame(False)#设置边框是否可见
    """
    绘制窗口部分
    """
    def paintEvent(self, event):
        """
        自动调用的一个函数，作用画图
        :param event:
        :return:
        """
        painter = QPainter(self)
        self.DrawReceipt(painter)
    def TableXY(self):
        """
        此函数的功能是定义QPainter绘图是绘图的坐标
        :return:None
        """
        x = 5
        y = 150
        self.width1 = 100
        self.width2 = 190
        self.height =40
        self.width =90
        self.sum_width = 160
        self.beizu_width = 110

        self.Cell = []
        for i in range(8):
            l = []
            for j in range(5):
                if j == 0:
                    l.append(Cell_Set(x, y + self.height * i, self.width1, self.height))
                elif j == 1:
                    l.append(Cell_Set(x + self.width1, y + self.height * i, self.width2, self.height))
                else:
                    l.append(Cell_Set(x + self.width2 + self.width * (j - 2) + self.width1, y + self.height * i, self.width, self.height))
            self.Cell.append(l)
        self.Change_cell = []
        for i in range(7):
            l = []
            for j in range(8):
                l.append(Cell_Set(self.Cell[1][4].x + self.width + 20 * j, self.Cell[1][4].y + self.height * i, 20, self.height))
            self.Change_cell.append(l)
        self.customer = Cell_Set(self.Cell[0][0].x + 20, self.Cell[0][0].y - 5,0,0)
        self.time = []
        for i in range(3):
            self.time.append(Cell_Set(self.Cell[0][0].x + 710 + 50 * i, self.Cell[0][0].y - 5,0,0))
        self.heji_width = 0
        for i in range(5):
            self.heji_width += self.Cell[0][i].width
        for i in range(8):
            self.heji_width += self.Change_cell[0][i].width
        self.heji = Cell_Set(self.Cell[0][0].x, self.Cell[7][0].y + self.height, self.heji_width, self.height)
        self.title2_cell = []  ######
        for i in range(8):
            self.title2_cell.append(Cell_Set(self.Cell[7][1].x + self.height + 52 * i + 20, self.heji.y + self.height - 10, 0, 0))
        self.title3_Cell=[]
        for i in range(3):
            self.title3_Cell.append(Cell_Set(self.heji.x + 20 + 250 * i, self.heji.y + self.height + 20,0,0))

        self.beizhu = Cell_Set(self.Cell[0][4].x + self.sum_width + self.width, self.Cell[0][4].y, self.beizu_width, self.height)
        self.beizhunext = Cell_Set(self.beizhu.x, self.beizhu.y + self.height, self.beizhu.width, self.height * 8)
    def DrawReceipt(self, painter):
        width = self.width
        sum_width = self.sum_width
        height = self.height

        name1 = "金  光  不  銹  鋼  收  款  收  據"
        company_name = "瀚   桌   实   业   有   限   公  司"
        address = "地址：东莞市东城街道温塘社区莞温路303栋3-5号     QQ：2756770568"
        Tel = "电话：0769-26622459  13712224520  13424864880  传真：23328962"
        head = [" 货 号 ", "  货 物 名 称  ", " 单 位 ", " 数 量 ", " 单 价 "]
        title = ["十", "万", "千", "百", "十", "元", "角", "分"]
        title2 = ["拾", "万", "仟", "佰", "拾", "元", "角", "分"]
        title3 = ["会计：", "出纳：", "填票人："]
        title4 = ["年", "月", "日"]
        title5 = ["存", "根", "白", "客", "户", "红", "会", "计", "黄", "回", "单", "蓝"]
        # 设置单元格的x,y,width,height
        # 绘制单元格
        for i in range(8):
            for j in range(5):
                painter.drawRect(self.Cell[i][j].x, self.Cell[i][j].y, self.Cell[i][j].width, self.Cell[i][j].height)
        painter.drawRect(self.Cell[0][4].x + width, self.Cell[0][4].y, sum_width, self.Cell[0][4].height / 2)
        for i in range(8):
            painter.drawRect(self.Cell[0][4].x + width + 20 * i, self.Cell[0][4].y + height / 2, sum_width // 8,
                             self.Cell[0][4].height / 2)
        for i in range(7):
            for j in range(8):
                painter.drawRect(self.Change_cell[i][j].x, self.Change_cell[i][j].y, self.Change_cell[i][j].width,
                                 self.Change_cell[i][j].height)
        painter.drawRect(self.beizhu.x, self.beizhu.y, self.beizhu.width, self.beizhu.height)
        painter.drawRect(self.beizhunext.x, self.beizhunext.y, self.beizhunext.width, self.beizhunext.height)
        painter.drawRect(self.heji.x, self.heji.y, self.heji_width, self.heji.height)
        # 写入文字
        x0 = 90
        painter.drawText(self.Cell[0][1].x + x0, self.Cell[0][1].y - 60, address)
        painter.drawText(self.Cell[0][1].x + x0, self.Cell[0][1].y - 40, Tel)
        painter.setFont(QFont("微软雅黑", 16, QFont.Bold))
        painter.drawText(self.Cell[0][1].x + x0, self.Cell[0][1].y - 80, company_name)
        painter.drawText(self.Cell[0][1].x + x0, self.Cell[0][1].y - 110, name1)
        painter.setFont(QFont("微软雅黑", 16))
        painter.drawText(self.Change_cell[0][0].x + 60, self.Change_cell[0][0].y - 120, "N")
        font = QFont("微软雅黑", 12, QFont.Bold)
        font.setUnderline(True)
        painter.setFont(font)
        painter.drawText(self.Change_cell[0][0].x + 80,self.Change_cell[0][0].y - 120, "0")
        painter.setFont(QFont("微软雅黑", 16, QFont.Bold))
        painter.setPen(QColor(Qt.red))
        painter.drawText(self.Change_cell[0][0].x + 100, self.Change_cell[0][0].y - 120, "0002201")
        # 设置字体格式
        painter.setFont(QFont("微软雅黑", 12, QFont.Bold))
        painter.setPen(QColor(Qt.black))
        painter.drawText(self.customer.x, self.customer.y, "客户：")
        for i in range(3):
            painter.drawText(self.time[i].x, self.time[i].y,title4[i])
        for i in range(5):
            painter.drawText(QRect(self.Cell[0][i].x, self.Cell[0][i].y, self.Cell[0][i].width, self.Cell[0][i].height), Qt.AlignCenter,
                             head[i])
        painter.drawText(QRect(self.Cell[0][4].x + width, self.Cell[0][4].y, sum_width, self.Cell[0][4].height / 2), Qt.AlignCenter,
                         "  金 额  ")
        for i in range(8):
            painter.drawText(
                QRect(self.Cell[0][4].x + width + 20 * i, self.Cell[0][4].y + height / 2, sum_width // 8, self.Cell[0][4].height / 2),
                Qt.AlignCenter, title[i])
        painter.drawText(QRect(self.beizhu.x, self.beizhu.y, self.beizhu.width, self.beizhu.height), Qt.AlignCenter, " 备 注 ")
        painter.drawText(self.heji.x, self.heji.y + height / 2 - 3, "合计人民币")
        painter.drawText(self.heji.x, self.heji.y + height - 5, "   (大写)")
        for i in range(8):
            painter.drawText(self.title2_cell[i].x, self.title2_cell[i].y, title2[i])
        painter.drawText(self.title2_cell[7].x + 30, self.title2_cell[i].y, "¥ :")
        # 添加下划线
        font = QFont("微软雅黑", 12, QFont.Bold)
        font.setUnderline(True)
        painter.setFont(font)
        painter.drawText(self.title2_cell[7].x + 55, self.title2_cell[i].y + 5, "                      ")
        painter.setFont(QFont("微软雅黑", 12, QFont.Bold))
        for i in range(3):
            painter.drawText(self.title3_Cell[i].x, self.title3_Cell[i].y , title3[i])
        painter.setFont(QFont("微软雅黑", 10, ))
        for i in range(12):
            if i % 3 == 0:
                painter.drawText(self.beizhunext.x + self.beizhunext.width + 5, self.beizhunext.y + 25 * i, title5[i])
            elif i % 3 == 1:
                painter.drawText(self.beizhunext.x + self.beizhunext.width + 5, self.beizhunext.y + 25 * i - 9, title5[i])
            else:
                painter.drawText(self.beizhunext.x + self.beizhunext.width + 5, self.beizhunext.y + 25 * i - 9, title5[i])
        painter.rotate(90)
        painter.rotate(0)
        base_y = self.beizhunext.y + 20
        base_y1 = self.beizhunext.y + 45
        for i in range(4):
            painter.drawText(base_y + 75 * i, -(self.beizhunext.x + self.beizhunext.width + 10), "(")
            painter.drawText(base_y1 + 75 * i, -(self.beizhunext.x + self.beizhunext.width + 10), ")")
    """
    打印
    """
    def GetImageFile(self):
        fname, _  = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.gif)")
        self.imagelabel.setPixmap(QPixmap(fname))
    def Print(self):
        title = ["红色(客户)","白色(存根)","黄色(会计)","蓝色(回单)"]
        for i in range(7):
            if  self.commoditydata.Find(self.lineedits[i][0].text())==False:
                self.commoditydata.InsertData(self.lineedits[i][0].text(),self.lineedits[i][1].text(),self.lineedits[i][2].text())
        for i in range(4):
            preview = QPrintPreviewDialog(self.printer, self)
            preview.setGeometry(100, 100, 1200, 600)
            if i==0:
                self.redcheckbutton.setChecked(True)
                self.colorlabel.setStyleSheet("background-color:rgba(255,0,0,25)")
            elif i==1:
                self.whitecheckbutton.setChecked(True)
                self.colorlabel.setStyleSheet("background-color:rgba(255,255,255,25)")
            elif i == 2:
                self.yellowcheckbutton.setChecked(True)
                self.colorlabel.setStyleSheet("background-color:rgba(255,255,0,25)")
            else:
                self.bluecheckbutton.setChecked(True)
                self.colorlabel.setStyleSheet("background-color:rgba(0,255,255,25)")
            preview.setWindowTitle(title[i])
            """
            以下两句实现控制打印纸张的大小
            QSizeF 中的第二个参数是height ，第一个是width
            """
            #self.printer.setPageSize(QPrinter.Custom)
            self.printer.setPaperSize(QSizeF(900, 550), QPrinter.Point)
            preview.paintRequested.connect(self.PlotPic)
            preview.exec()#显示预览窗口
        self.colorlabel.setStyleSheet("background-color:rgba(255,255,255,25)")
        self.bluecheckbutton.setChecked(False)
    def PlotPic(self):
        painter = QPainter(self.printer)
        # QRect(0,0) 中（0,0）是窗口坐标
        image = self.grab(QRect(QPoint(0, 0),QSize(900,550) ) )  # /* 绘制窗口至画布 */
        # QRect
        rect = painter.viewport()
        # QSize
        size = image.size();
        size.scale(rect.size(), Qt.KeepAspectRatio)  # //此处保证图片显示完整
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(image.rect())
        painter.drawPixmap(0, 0, image);  # /* 数据显示至预览界面 */
if __name__ == '__main__':
    app = QApplication(sys.argv)
    commodity = Commodity()
    window = MyWindow(commodity)
    sys.exit(app.exec())