import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QPushButton,
                             QVBoxLayout,
                             QTableWidgetItem, QLabel, QFileDialog, QMainWindow, QFrame, QLineEdit, QRadioButton,
                             QToolButton, QGroupBox, QMessageBox, QListWidget, QDateTimeEdit, QHBoxLayout, QCheckBox)
from PyQt5.QtGui import QPixmap, QPainter, QImage, QTextDocument, QColor, QFont, QTextOption, QIcon
from PyQt5.QtPrintSupport import  QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QRect, QPoint, QSize, Qt, QSizeF, QDateTime
import sys
from CommodityData import Commodity
from KuCunData import KuCunDan
import YingYeEData
lower_to_upper = {"0":"零","1":"壹","2":"貳","3":"叁","4":"肆","5":"伍","6":"陆","7":"柒","8":"捌","9":"玖"}
title2 = ["拾", "万", "仟", "佰", "拾", "元", "角", "分"]
class Cell_Set():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
class MyWindow(QMainWindow):
    def __init__(self,commodity):
        super().__init__()
        self.commodityData = commodity
        self.kucundandata = KuCunDan(commodity)
        self.yingye = YingYeEData.YingYeE(commodity)
        self.initUI()
        self.show()

    def Show(self):
        if self.commodityData.model.tableName()!="yingyee":
            self.commodityData.model.setTable("yingyee")
            self.commodityData.model.select()
        self.yingye.show()
    def ShowNotPayCustomer(self):
        """
        点击listwidget的item时被调用
        显示未付款用户
        :return:
        """
        select = self.listwidget.currentItem().text().split()
        kehu=self.kucundandata.Find("name",select[0],"==")
        if kehu:
            alldata = self.kucundandata.getData("date",select[1]+" "+select[2],"==")
            self.FillTable(alldata[0])
    def FillTable(self,data):
        """
        此函数用于将数据库中的未付款客户数据展示在界面上，被ShowNotPayCustomer调用
        :param data:
        :return:
        """
        a = data[0].split()
        self.dateedit.setText(a[0])
        self.customer.setText(data[1])
        self.danjubianhao.setText(data[2])
        self.chuhuocangku.setText(data[3])
        self.customertel.setText(data[4])
        self.address.setText(data[5])
        for i in range(6,11):
            self.beizhulineedits[i-6].setText(data[i])
        index = 11
        for i in range(10):
            if data[(index-11)%8==0]!="":
                for j in range(8):
                    self.lineedits[i][j].setText(data[index])
                    index+=1
            else:
                break
    def LineEditsEditAble(self,Bool):
        """
        设置表格是否可以编辑，在查看未付款用户下不可编辑,打开或关闭都会清空单据
        :param Bool:
        :return:
        """
        self.dateedit.setReadOnly(Bool)
        self.customer.setReadOnly(Bool)
        self.danjubianhao.setReadOnly(Bool)
        self.chuhuocangku.setReadOnly(Bool)
        self.customertel.setReadOnly(Bool)
        self.address.setReadOnly(Bool)
        for i in range(6, 11):
            self.beizhulineedits[i - 6].setReadOnly(Bool)
        for i in range(10):
            for j in range(8):
                self.lineedits[i][j].setReadOnly(Bool)
        self.dateedit.setText("")
        self.customer.setText("")
        self.danjubianhao.setText("")
        self.chuhuocangku.setText("")
        self.customertel.setText("")
        self.address.setText("")
        for i in range(6, 11):
            self.beizhulineedits[i - 6].setText("")
        for i in range(10):
            for j in range(8):
                self.lineedits[i][j].setText("")

    def getcheckrange(self):
        """
        获得查找未付款客户的范围
        :return:
        """
        self.datetimemax = QDateTimeEdit(QDateTime.currentDateTime(), self)  # 3
        self.datetimemax.dateTimeChanged.connect(lambda: print(self.datetimemax.text()))
        self.datetimemax.setCalendarPopup(True)
        self.datetimemin = QDateTimeEdit(QDateTime.currentDateTime(), self)  # 3
        self.datetimemin.dateTimeChanged.connect(lambda: print(self.datetimemin.text()))
        self.datetimemin.setCalendarPopup(True)
        #self.datetimemin.setReadOnly(True)
        #self.datetimemax.setReadOnly(True)

        groupbox = QGroupBox("查看模式选择",self.listframe)
        min = QLabel("起始日期：")
        max = QLabel("终止日期：")
        kehulabel = QLabel("客户名称：")
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout1.addStretch(1)
        hlayout2.addStretch(1)
        hlayout1.addWidget(min)
        hlayout1.addWidget(self.datetimemin)
        hlayout2.addWidget(max)
        hlayout2.addWidget(self.datetimemax)
        hlayout3 = QHBoxLayout()
        hlayout3.addStretch(1)
        hlayout3.addWidget(kehulabel)

        self.kehucheckbox = QCheckBox("按客户查找")
        self.datecheckbox = QCheckBox("按日期查找")
        self.findcustomer = QLineEdit("")
        hlayout3.addWidget(self.findcustomer)
        #self.findcustomer.setReadOnly(True)
        #self.finddate = QLineEdit()
        vlayout = QVBoxLayout()
        vlayout.addStretch(1)
        vlayout.addWidget(self.kehucheckbox)
        vlayout.addLayout(hlayout3)
        vlayout.addWidget(self.datecheckbox)
        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)
        groupbox.setLayout(vlayout)
        self.findbutton = QPushButton(groupbox)
        self.findbutton.setGeometry(200, 15, 35, 35)
        self.findbutton.setIcon(QIcon("find.jpg"))
        #self.findbutton.setStyleSheet("border-width:30px")
        #self.findbutton.autoFillBackground()
        self.findbutton.setToolTip("查找")
        self.findbutton.clicked.connect(self.ChooseFindWay)

    def ChooseFindWay(self):
        if self.kehucheckbox.isChecked() and not self.datecheckbox.isChecked():
            if self.findcustomer.text()!="":
                self.listwidget.clear()
                print("1")

                self.AddListItem(self.kucundandata.getData("name",self.findcustomer.text(),"=="))
                print("哈哈哈哈哈哈哈哈")
        elif self.kehucheckbox.isChecked() and self.datecheckbox.isChecked():
            dataname = self.kucundandata.getData("name",self.findcustomer.text(),"==")
            adddata =[]
            if dataname ==None:
                QMessageBox.information(self,"注意","未发现该客户")
                return
            min = (self.datetimemin.text().split())[0]
            max = (self.datetimemax.text().split())[0]
            if min>max:
                QMessageBox.warning(self, "错误提示", "请输入正确的时间范围")
                return
            else:
                min += " 00:00:00"
                max += " 23:59:59"
                data1 = self.kucundandata.getData("date", min, ">=")
                data2 = self.kucundandata.getData("date", max, "<=")
                if data1 != None and data2 != None:
                    for data in data1:
                        if data in data2:
                            if data in dataname:
                                adddata.append(data)
                self.listwidget.clear()
                self.AddListItem(adddata)
        elif self.datecheckbox.isChecked() and not self.kehucheckbox.isChecked():
            min = (self.datetimemin.text().split())[0]
            max = (self.datetimemax.text().split())[0]
            if min>max:
                QMessageBox.warning(self,"错误提示","请输入正确的时间范围")
                return
            else:
                min+=" 00:00:00"
                max+=" 23:59:59"
                data1 = self.kucundandata.getData("date",min,">=")
                data2 = self.kucundandata.getData("date",max,"<=")
                self.listwidget.clear()
                if data1!=None and data2 !=None:
                    data3=[]
                    for data in data1:
                        if data in data2:
                            data3.append(data)
                    print("-----",data3)
                    if len(data3)!=0:
                        self.AddListItem(data3)
        else:
            year = datetime.date.today().year + 1
            self.AddListItem(self.kucundandata.getData('date', str(year), "<="))
            QMessageBox.information(self, "提示", "请勾选查询方式")




    def deletecustomer(self):
        """
        删除未付款客户，此处还需要将此客户从数据库中删除，并将未付款状态修改成已付款状态
        :return:
        """
        result=QMessageBox.information(self,"提示","确定删除此未付客户？",QMessageBox.Yes|QMessageBox.No)
        if result == QMessageBox.Yes:
            date=self.listwidget.currentItem().text().split()
            target = date[1]+" "+date[2]
            self.kucundandata.RemoveData("date",target,"==")
            self.yingye.ReviseStatus(target,"已付款")
            self.listwidget.takeItem(self.listwidget.currentIndex().row())
    def AddListItem(self,data):
        """
        :param data: data 是数据库中getData获得的数据，是一个二位列表
        :return:
        """
        if data ==None:
            QMessageBox.information(self,"查找结果","未发现该客户")
            return
        print(data)
        print("AddListItem")
        self.listwidget.clear()
        listdata = [data[i][1]+"       "+data[i][0] for i in range(0,len(data)) ]
        self.listwidget.addItems(listdata)



    def initUI(self):
        self.setGeometry(200, 200, 1000, 800)
        self.setStyleSheet("background-color:rgb(255,255,255,255)")
        self.setWindowIcon(QIcon("n.jpg"))
        self.setWindowTitle("库存单")
        self.listframe = QFrame(self)
        self.listwidget = QListWidget(self.listframe)
        self.listwidget.setGeometry(0,175,300,455)
        #self.listwidget.addItems(["黄小泽    2018/11/25 16:32:04","小黄    2018-10-30","小泽  2018-9-31"])
        self.listframe.setVisible(False)
        self.listframe.setGeometry(950,0,300,800)
        #self.listframe.setStyleSheet("background-color:blue")

        self.listwidget.itemClicked.connect(self.ShowNotPayCustomer)
        self.listwidget.itemDoubleClicked.connect(self.deletecustomer)

        self.closelistbutton = QPushButton("关闭",self.listframe)
        self.closelistbutton.setGeometry(100,650,50,25)
        self.closelistbutton.clicked.connect(lambda:self.ShowNotPay(False))
        self.getcheckrange()
        self.TableXY()
        label = QLabel(self)
        label.setFont(QFont("微软雅黑", 9, QFont.Bold))
        label.setGeometry(self.Cell[0][8].x + 155, self.Cell[0][8].y - 115, 29, 625)
        label.setText("白\n联\n存\n根\n\n红\n联\n收\n款\n签\n名\n作\n欠\n款\n依\n据\n \n蓝\n联\n仓\n库\n \n黄\n联\n客\n户")
        self.Write()
        self.ChoosePrintColor()
        self.LineEdit()
    def ShowNotPay(self,a):
        """
        显示未付款客户，以及打开数据库的'sh'或'Kucun'table
        :param a: bool
        :return:
        """
        if a==False:#填写模式
            print("close")
            self.commodityData.model.setTable("sh")
            self.setGeometry(200, 200, 1000, 800)
            self.listframe.setVisible(False)
            self.LineEditsEditAble(False)
            self.groupbox2.setVisible(True)
            self.AddinDatabase = True   #定义这个变量的目的是为了传递此时是否是处于查看模式，以便阻止将数据存入数据库

            self.listwidget.clear()
        else:#查看模式
            self.commodityData.model.setTable("Kucun")
            self.setGeometry(200, 200, 1400, 800)
            self.listframe.setVisible(True)
            self.LineEditsEditAble(True)
            self.groupbox2.setVisible(False)
            year = datetime.date.today().year+1
            self.AddinDatabase= False
            self.AddListItem(self.kucundandata.getData('date',str(year),"<="))

    def ChoosePrintColor(self):
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printerbutton = QPushButton("打印", self)
        self.printerbutton.setStyleSheet("background-color:rgb(240,128,128,250)")
        self.printerbutton.setGeometry(200, 650, 50, 50)
        self.printerbutton.clicked.connect(self.Print)
        self.checkpay = QPushButton("查看未付款",self)
        self.checkpay.setStyleSheet("background-color:rgb(240,128,128,250)")
        self.checkpay.clicked.connect(lambda:self.ShowNotPay(True))
        self.checkpay.setGeometry(300,650,100,50)
        self.colorlabel = QLabel(self)
        self.colorlabel.setGeometry(0, 0, 940, 630)
        self.colorlabel.setFrameShape(QFrame.Box)
        self.colorlabel.setStyleSheet("background-color:rgb(255,0,0,0)")
        self.redcheckbutton = QRadioButton("红色(客户)")
        self.whitecheckbutton = QRadioButton("白色(存根)")
        self.yellowcheckbutton = QRadioButton("黄色(会计)")
        self.bluecheckbutton = QRadioButton("蓝色(回单)")
        self.whitecheckbutton.setChecked(True)
        frame = QFrame(self)
        frame.setGeometry(700, 630, 120, 140)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.whitecheckbutton)
        vlayout.addWidget(self.yellowcheckbutton)
        vlayout.addWidget(self.bluecheckbutton)
        vlayout.addWidget(self.redcheckbutton)
        vlayout.addStretch(1)
        groupbox1 = QGroupBox("颜色",frame)
        groupbox1.setLayout(vlayout)
        self.yifu = QRadioButton("已付款")
        self.weifu = QRadioButton("未付款")
        vlayout1 = QVBoxLayout()
        vlayout1.addStretch(1)
        vlayout1.addWidget(self.yifu)
        vlayout1.addWidget(self.weifu)
        self.groupbox2 = QGroupBox("付款情况",self)
        self.groupbox2.setLayout(vlayout1)
        self.groupbox2.setGeometry(570, 630, 120, 90)
        self.yifu.toggled.connect(self.addcustomer)
        self.weifu.toggled.connect(self.addcustomer)

    def getYingYeEData(self,status):
        data=[]
        if self.weifu.isChecked():
            data.append(self.yingyeedate)#确保该客户与未付款库存单的日期一致
        else:
            data.append(self.dateedit.text() + datetime.datetime.now().strftime(' %H:%M:%S'))
        data.append(self.customer.text())
        data.append(self.sumlabel.text())
        data.append(status)
        print(data)
        return data

    def CheckTable(self):
        if self.customer.text()=="" or self.danjubianhao.text()=="" \
                or self.chuhuocangku.text()=="" or self.customertel.text()=="" or self.address.text()=="" or self.dateedit.text()=="":
            QMessageBox.warning(self,"注意","请将库存单信息填完整")
            return False
        for i in range(4):
            if self.beizhulineedits[i].text()=="":
                QMessageBox.warning(self,"注意","请将库存单信息填完整")
                return False
        return True

    def getnotpaydata(self):
        """
        次函数用于获得未付款的数据，便于存于数据库
        :return:
        """
        data =[]
        data.append(self.dateedit.text()+ datetime.datetime.now().strftime(' %H:%M:%S') )# 需要加上本地时间保证订单唯一性
        self.yingyeedate = data[0]
        data.append(self.customer.text())
        data.append(self.danjubianhao.text())
        data.append(self.chuhuocangku.text())
        data.append(self.customertel.text())
        data.append(self.address.text())
        for i in range(5):
            data.append(self.beizhulineedits[i].text())
        for i in range(10):
            for j in range(8):
                data.append(self.lineedits[i][j].text())
        return data



    def addcustomer(self):
        if self.yifu.isChecked():
            print("已付款")
        else:
            print("未付款")








    def filltable(self):
        """
        填写表格的数量和单价时自动补全
        :return: None
        """
        heji = 0
        amount=0
        print("func:filltable")
        for i in range(10):
            if self.lineedits[i][4].text()!="" and self.lineedits[i][5].text()!="":
                total = float(self.lineedits[i][4].text())*float(self.lineedits[i][5].text())
                heji+=total
                amount+=float(self.lineedits[i][4].text())
                self.lineedits[i][6].setText(str(total))
            else:
                self.lineedits[i][6].setText("")
        if heji!=0:
            h = str(int(heji*100))
            change =""
            print(h)
            for i in range(1,len(h)+1):
                t = lower_to_upper[h[-i]]+title2[-i]
                change=t+change
            self.hejilabel.setText(change)
            self.amountlabel.setText(str(amount))
            self.sumlabel.setText(str(heji))
        else:
            self.hejilabel.setText("")
            self.amountlabel.setText("")
            self.sumlabel.setText("")
    def CheckData(self):
        """
        填写表格的编号时自动补全
        :return:
        """
        print("func:CheckData")
        for i in range(10):
            if self.commodityData.Find(self.lineedits[i][0].text()):
                k = self.commodityData.getData(self.lineedits[i][0].text())
                for j in range(1, 3):
                    self.lineedits[i][j].setText(k[j])
    def LineEdit(self):
        """
        定义表格的lineedit对象
        :return:
        """
        self.lineedits = [[QLineEdit(self) for col in range(8) ] for row in range(10)]
        for i in range(10):
            for j in range(8):
                self.lineedits[i][j].setGeometry(self.Cell[i+1][j+1].x,self.Cell[i+1][j+1].y,self.Cell[i+1][j+1].width,self.Cell[i+1][j+1].height)
                self.lineedits[i][j].setStyleSheet("background-color:rgb(0,0,0,0)")
                self.lineedits[i][j].setFrame(False)
                if j==4 or j==5:
                    self.lineedits[i][j].textChanged.connect(self.filltable)
                elif j==0:
                    self.lineedits[i][j].textChanged.connect(self.CheckData)

        self.beizhulineedits = [QLineEdit(self) for i in range(5)]
        for i in range(5):
            self.beizhulineedits[i].setStyleSheet("background:rgb(0,0,0,0)")
            self.beizhulineedits[i].setFrame(QFrame.NoFrame)
            self.beizhulineedits[i].setFont(QFont("微软雅黑",9,QFont.Bold))
            if i ==0:
                self.beizhulineedits[i].setGeometry(self.beizhuxy[i].x+50,self.beizhuxy[i].y-20,100,30)
            elif i<4 and i>0:
                self.beizhulineedits[i].setGeometry(self.beizhuxy[i].x + 70, self.beizhuxy[i].y-20, 100, 30)
            else:
                self.beizhulineedits[i].setGeometry(self.beizhuxy[i].x + 170, self.beizhuxy[i].y-20, 60, 30)
        self.dateedit = QLineEdit(self)
        self.dateedit.setFrame(QFrame.NoFrame)
        self.dateedit.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.dateedit.setGeometry(self.Cell[0][8].x-20, self.Cell[0][2].y - 2 * self.height- 28, 190, 25)
        self.danjubianhao = QLineEdit(self)
        self.danjubianhao.setFrame(QFrame.NoFrame)
        self.danjubianhao.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.danjubianhao.setGeometry(self.Cell[0][8].x-20, self.Cell[0][2].y - 2 * self.height , 190, 25)
        self.chuhuocangku = QLineEdit(self)
        self.chuhuocangku.setFrame(QFrame.NoFrame)
        self.chuhuocangku.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.chuhuocangku.setGeometry(self.Cell[0][0].x+80, self.Cell[0][0].y - 50, 220,25)
        self.customertel = QLineEdit(self)
        self.customertel.setFrame(QFrame.NoFrame)
        self.customertel.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.customertel.setGeometry(self.Cell[0][0].x+80, self.Cell[0][0].y - 25, 220, 25)
        self.customer = QLineEdit(self)
        self.customer.setFrame(QFrame.NoFrame)
        self.customer.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.customer.setGeometry(self.Cell[0][3].x+45, self.Cell[0][3].y - 50, 200, 25)
        self.address = QLineEdit(self)
        self.address.setFrame(QFrame.NoFrame)
        self.address.setStyleSheet("background-color:rgb(0,0,0,0)")
        self.address.setGeometry(self.Cell[0][3].x+45, self.Cell[0][3].y - 25, 300, 25)
    def TableXY(self):
        """
        定义表格的单元格的长宽
        :return:
        """
        self.x =10
        self.y = 125
        self.height=32
        self.Cell =[]
        self.colwidth = {1:32,2:80,3:200,4:50,5:150,6:80,7:80,8:80,9:150}
        for i in range(11):
            l = []
            for j in range(9):
                x =0
                for z in range(j):
                    x+=self.colwidth[z+1]
                l.append(Cell_Set(x+self.x,self.height*i+self.y,self.colwidth[j+1],self.height))
            self.Cell.append(l)
        self.zhidan = Cell_Set(self.Cell[10][0].x+10, self.Cell[10][0].y+175 ,0,0)
        self.jingshouren=Cell_Set(self.Cell[10][0].x + 170, self.Cell[10][0].y+175 ,0,0)
        self.shoukuangren = Cell_Set(self.Cell[10][0].x + 340, self.Cell[10][0].y+175 ,0,0)
        self.fahuoren = Cell_Set(self.Cell[10][0].x +510, self.Cell[10][0].y +175,0,0 )
        self.kehu = Cell_Set(self.Cell[10][0].x + 700, self.Cell[10][0].y+175 ,0,0)
        self.beizhuxy = [self.zhidan,self.jingshouren,self.shoukuangren,self.fahuoren,self.kehu]
    def Write(self):
        """
        在屏幕上画上库存单合计及以下的内容
        :return:
        """
        self.jiaoyi = QLabel(self)
        self.jiaoyi.setFont(QFont("微软雅黑",10,QFont.Bold))
        self.jiaoyi.setGeometry(self.Cell[10][0].x,self.Cell[10][0].y+62,890,97)
        self.jiaoyi.setText("交易协议：1.客户收货时请当面核对数量、质量，如有质量问题请于签收后三天内提出异议，超期通知我司将不予处理。\n"
                            "2.*****价差损失负责，对所造成的期待利益、下家损失、商誉损失均不承担责任。"
                            "3.此单作为买卖双方****合同，\n*****************买方必须在当天内付清贷款，逾期每天按总金额1%加收违约金。\n"
                            )
        self.jiaoyi.setStyleSheet("background-color:rgb(0,0,0,0)")
        beizu = QLabel("备注：",self)
        beizu.setFont(QFont("微软雅黑",12,QFont.Bold))
        beizu.setGeometry(self.Cell[10][0].x,self.Cell[10][0].y+129,50,25)
        beizu.setStyleSheet("background-color:rgb(0,0,0,0)")

        width1 =0
        width2 =0
        for i in range(7):
            if i <5:
                width1 += self.Cell[0][i].width
            else:
                width2 += self.Cell[0][i].width
        label2 = QLabel("合计：",self)
        label2.setFont(QFont("微软雅黑",10,QFont.Bold))
        label2.setGeometry(self.Cell[10][0].x,self.Cell[10][0].y+self.height,width1+1,self.height)
        label2.setFrameShape(QFrame.Box)
        self.amountlabel = QLabel(self)
        self.amountlabel.setGeometry(self.Cell[10][5].x,self.Cell[10][0].y+self.height,width2+1,self.height)
        self.amountlabel.setFrameShape(QFrame.Box)
        self.sumlabel = QLabel(self)
        self.sumlabel.setGeometry(self.Cell[10][7].x, self.Cell[10][0].y + self.height, self.Cell[10][7].width+1, self.height)
        self.sumlabel.setFrameShape(QFrame.Box)
        label5 = QLabel(self)
        label5.setGeometry(self.Cell[10][8].x, self.Cell[10][0].y + self.height, self.Cell[10][8].width+1, self.height)
        label5.setFrameShape(QFrame.Box)
        label2.setStyleSheet("background-color:rgb(255,0,0,0)")
        label5.setStyleSheet("background-color:rgb(255,0,0,0)")
        self.hejilabel = QLabel(self)
        self.hejilabel.setGeometry(self.Cell[10][0].x+60,self.Cell[10][0].y+self.height,width1+1,self.height)
        self.hejilabel.setStyleSheet("background-color:rgb(255,0,0,0)")
        self.amountlabel.setStyleSheet("background-color:rgb(255,0,0,0)")
        self.sumlabel.setStyleSheet("background-color:rgb(255,0,0,0)")
    def paintEvent(self,event):
        painter = QPainter(self)
        self.DrawReceipt(painter)
    def DrawReceipt(self, painter):
        title = "东莞市天航五金制品有限公司 销售出库单"
        address = "地址：东莞市东城区温塘红槟榔东日仓库3号"
        tel = "电话：0769-23831842 81805899 传真：0769-27205560"
        title1 =["No.","商品编号","   商 品 名 称   ","单位","   规 格   "," 数 量 "," 单 价 "," 金 额 ","   备 注   "]
        for i in range(11):
            for j in range(9):
                painter.drawRect(self.Cell[i][j].x,self.Cell[i][j].y,self.Cell[i][j].width,self.Cell[i][j].height)
        #填入文字
        painter.setFont(QFont("微软雅黑", 16, QFont.Bold))
        painter.drawText(QRect(self.Cell[0][2].x-6,self.Cell[0][2].y-3*self.height-25,550,40),Qt.AlignCenter,title)
        painter.setFont(QFont("微软雅黑",10,QFont.Bold))
        painter.drawText(QRect(self.Cell[0][2].x +50, self.Cell[0][2].y - 2 * self.height - 33, 350, 40),Qt.AlignCenter, address)
        painter.drawText(QRect(self.Cell[0][8].x -100, self.Cell[0][2].y - 2 * self.height - 35, 100, 40),Qt.AlignCenter, "销售日期：")
        painter.drawText(QRect(self.Cell[0][2].x - 3, self.Cell[0][2].y -  2*self.height - 14, 500, 40),Qt.AlignCenter, tel)
        painter.drawText(QRect(self.Cell[0][8].x-100 , self.Cell[0][2].y - 2 * self.height - 10, 100, 40), Qt.AlignCenter, "单据编号：")
        painter.drawText(QRect(self.Cell[0][0].x-6,self.Cell[0][0].y-self.height-25,100,40),Qt.AlignCenter,"出货仓库：")
        painter.drawText(QRect(self.Cell[0][0].x-6,self.Cell[0][0].y-self.height,100,40),Qt.AlignCenter,"客户电话：")
        painter.drawText(QRect(self.Cell[0][3].x - 22, self.Cell[0][3].y - self.height - 25, 100, 40), Qt.AlignCenter,"客户：")
        painter.drawText(QRect(self.Cell[0][3].x - 22, self.Cell[0][3].y - self.height, 100, 40), Qt.AlignCenter,"地址：")
        for i in range(1,11):
            painter.drawText(QRect(self.Cell[0][0].x,self.Cell[i][0].y,self.Cell[i][0].width,self.Cell[i][0].height),Qt.AlignCenter,str(i))
        for j in range(9):
            painter.drawText(QRect(self.Cell[0][j].x,self.Cell[0][j].y,self.Cell[0][j].width,self.Cell[0][j].height),Qt.AlignCenter,title1[j])
        painter.setFont(QFont("微软雅黑",12,QFont.Bold))
        painter.drawText(self.zhidan.x,self.zhidan.y, "制单：")
        painter.drawText(self.jingshouren.x,self.jingshouren.y, "经手人：")
        painter.drawText(self.shoukuangren.x,self.shoukuangren.y, "收款人：")
        painter.drawText(self.fahuoren.x,self.fahuoren.y, "发货人：")
        painter.drawText(self.kehu.x,self.kehu.y, "客户签字（盖章）：")
        pixmap = QPixmap("607.jpg")
        painter.setOpacity(0.65)
        painter.drawPixmap(QRect(0,632,1500,200), pixmap)

    """
     打印
     """
    def Print(self):
        if self.CheckTable()==False:#如果库存单信息不完整，将不能打印
            return

        if  not(self.yifu.isChecked() or  self.weifu.isChecked()) and self.AddinDatabase==True:
            QMessageBox.warning(self,"警告","请选择“付款情况")
            return

        if self.AddinDatabase:#在非查看模式下打印才会将数据存入数据库
        #if True:
            print("yes")
            if not self.yifu.isChecked():#将未付款客户订单存入数据库
                print(self.getnotpaydata())
                self.kucundandata.InsertData(self.getnotpaydata())
                self.yingye.InsertData(self.getYingYeEData("未付款"))
                #print(self.getYingYeEData("未付款"))
            else:
                self.yingye.InsertData(self.getYingYeEData("已付款"))
                #print(self.getYingYeEData("已付款"))
            for i in range(10):#将从没出现过的商品存入数据库
                if  self.commodityData.Find(self.lineedits[i][0].text())==False:
                    self.commodityData.InsertData(self.lineedits[i][0].text(),self.lineedits[i][1].text(),self.lineedits[i][2].text())


        for i in range(4):
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
            preview = QPrintPreviewDialog(self.printer,self)
            preview.setGeometry(100, 100, 1200, 900)
            """
            以下两句实现控制打印纸张的大小
            QSizeF 中的第二个参数是height ，第一个是width
            """
            self.printer.setPageSize(QPrinter.Custom)
            self.printer.setPaperSize(QSizeF(1880, 1260), QPrinter.Point)#QSizeF 中的参数按比例改变可以填充满纸张
            preview.paintRequested.connect(self.PlotPic)
            preview.exec()  # 显示预览窗口

        self.colorlabel.setStyleSheet("background-color:rgba(255,255,255,25)")
        self.bluecheckbutton.setChecked(False)
    def PlotPic(self):
        painter = QPainter(self.printer)
        # QRect(0,0) 中（0,0）是窗口坐标
        image = self.grab(QRect(QPoint(0, 0), QSize(940, 630)))  # /* 绘制窗口至画布 */
        rect = painter.viewport()
        size = image.size();
        size.scale(rect.size(), Qt.KeepAspectRatio)  # //此处保证图片显示完整
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(image.rect())
        painter.drawPixmap(0, 0, image);  # /* 数据显示至预览界面 */
"""
if __name__ =="__main__":
    app = QApplication(sys.argv)
    commodity = Commodity()
    win = MyWindow(commodity)
    sys.exit(app.exec_())


设计时还没有将多次点击打印的情况考虑好，感觉可以设置一个哨兵来控制
在查看状态下，应该可以打印。但是不会将数据存入数据库
可以选择打印那种颜色的库存单，可以

该程序可能存在的问题：
1.由于未付款用户的数据存入数据库时，是以时间保证唯一性，可能在查看模式下打印时又添加一遍----通过设置哨兵解决
2.尚未限制输入框允许输入的最大字数------很严重
3.考虑到技术不够家，防止在用的过程中出现意外，应该将所有数据都保存起来------很严重
4.打印纸张的大小
"""