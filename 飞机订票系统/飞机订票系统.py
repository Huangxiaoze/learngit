from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon, QFont, QPalette, QBrush
from PyQt5.QtWidgets import *
import sys
import register
import CheckTicket
import revise
import airplaneclass
from copy import copy
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.DataBase = airplaneclass.AirlineCompany()
        #测试数据
        self.DataBase.addpassenger("C:/Users/Hasee/PycharmProjects/image/8.jpg","黄小泽", "黄泽文", 15768497440, 1228, 44098, "1317670668@qq.com")
        self.DataBase.addadministrator("C:/Users/Hasee/PycharmProjects/image/7.jpg","黄小红", "黄小红", 15363159240, 1228, 12, 12)
        self.DataBase.addairplane(101, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00","2018/12/25/18:00")
        self.DataBase.addairplane(102, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/20/19:00", "2018/12/22/19:00","2018/12/24/19:00")
        self.DataBase.addairplane(111, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00",
                                  "2018/12/25/18:00")
        self.DataBase.addairplane(122, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/20/19:00", "2018/12/22/19:00",
                                  "2018/12/24/19:00")
        self.DataBase.addairplane(103, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/21/18:00", "2018/12/23/18:00",
                                  "2018/12/25/18:00")
        self.DataBase.addairplane(104, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/21/19:00", "2018/12/23/19:00",
                                  "2018/12/24/19:00")
        self.DataBase.addairplane(105, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/22/18:00", "2018/12/24/18:00",
                                  "2018/12/25/18:00")
        self.DataBase.addairplane(106, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/22/19:00", "2018/12/24/19:00",
                                  "2018/12/24/19:00")
        self.DataBase.addairplane(107, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/23/18:00", "2018/12/25/18:00",
                                  "2018/12/25/18:00")
        self.DataBase.addairplane(108, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/23/19:00", "2018/12/25/19:00",
                                  "2018/12/24/19:00")
        self.initUI()
        self.Lognin()
        self.addFlight()
        self.CheckAirplane()
        self.showResult()
    def Booking(self,i):
        print(i)
        s = self.result[i][1].text()
        s1=self.result[i][3].text()
        takeofftime=s[:10]+"/"+s[13:18]
        arrivetime = s1[:10]+"/"+s[13:18]
        print(takeofftime,arrivetime,"book")
        tag = self.DataBase.booking(int(self.usertel),int(self.result[i][0].text()),takeofftime,arrivetime)
        print("yes")
        if tag:
            self.result[i][5].setText(str(int(self.result[i][5].text())-1))
            if self.result[i][5].text()=="0":
                self.result[i][-1].setEnabled(False)
            print(self.DataBase.getpassengerticket(self.usertel))
            QMessageBox.information(self, "提示", str(i) + "成功订票")

    def Research(self):
        print("hahahaha")
        airplane1 = self.DataBase.findairplane(offcity=self.lineedits[0].text(),arrivecity=self.lineedits[1].text())
        airplane2 = self.DataBase.findairplane(takeofftime=self.lineedits[2].text(),arrivetime=self.lineedits[3].text())
        correspond = []
        for airplane in airplane1:
            if airplane in airplane2:
                correspond.append(airplane)
        print(correspond)
        if correspond!=[]:
            self.showairplane(correspond)
            QMessageBox.information(self,"提示","重新搜索成功")
        else:
            QMessageBox.information(self,"提示","Not Found!")

    def showResult(self):
        self.showsearchresultframe = QFrame(self)
        self.searchframe.setVisible(False)
        self.showsearchresultframe.setGeometry(200,100,900,900)
        #self.showsearchresultframe.setStyleSheet("background-color:rgb(0,255,0,25)")
        self.lineedits = [ QLineEdit(self.showsearchresultframe) for i in range(4)]
        self.lineedits[0].setPlaceholderText("起飞城市")
        self.lineedits[1].setPlaceholderText("到达城市")
        self.lineedits[2].setPlaceholderText("起飞时间")
        self.lineedits[3].setPlaceholderText("到达时间")
        for i in range(4):
            self.lineedits[i].setGeometry(10+i*110,10,100,25)
            self.lineedits[i].setFont(QFont("微软雅黑",10,QFont.Bold))
        self.research = QPushButton("重新搜索",self.showsearchresultframe)
        self.research.clicked.connect(self.Research)
        self.research.setGeometry(500,10,80,25)

        self.takeoffcity = QLabel(self.showsearchresultframe)
        self.arrivecity = QLabel(self.showsearchresultframe)
        self.arrow = QLabel("→",self.showsearchresultframe)
        self.takeoffcity.setFont(QFont("微软雅黑",24,QFont.Bold))
        self.arrivecity.setFont(QFont("微软雅黑", 24, QFont.Bold))
        self.arrow.setFont(QFont("微软雅黑", 24, QFont.Bold))
        self.takeoffcity.setGeometry(60,40,100,50)
        self.arrow.setGeometry(170,40,50,50)
        self.arrivecity.setGeometry(230,40,100,50)
        self.result = [[None for i in range(7)] for j in range(10)]
        for i in range(10):
            self.result[i][0]=QLabel("航班号",self.showsearchresultframe)
            self.result[i][1]=QLabel("出发日期\n出发时间\n出发机场",self.showsearchresultframe)
            self.result[i][2] =QLabel("→",self.showsearchresultframe)
            self.result[i][2].setFont(QFont("微软雅黑",16,QFont.Bold))
            self.result[i][3] =QLabel("抵达日期\n抵达时间\n抵达机场 ",self.showsearchresultframe)
            self.result[i][4] =QLabel("票价",self.showsearchresultframe)
            self.result[i][5] =QLabel("可定票数",self.showsearchresultframe)
            self.result[i][6] =QPushButton("订票",self.showsearchresultframe)
        self.result[1][6].clicked.connect(lambda :self.Booking(1))
        self.result[2][6].clicked.connect(lambda:self.Booking(2))
        self.result[3][6].clicked.connect(lambda: self.Booking(3))
        self.result[4][6].clicked.connect(lambda: self.Booking(4))
        self.result[5][6].clicked.connect(lambda: self.Booking(5))
        self.result[6][6].clicked.connect(lambda: self.Booking(6))
        self.result[7][6].clicked.connect(lambda: self.Booking(7))
        self.result[8][6].clicked.connect(lambda: self.Booking(8))
        self.result[9][6].clicked.connect(lambda: self.Booking(9))
        self.result[0][6].setVisible(False)
        y =100
        for i in range(10):
            self.result[i][0].setGeometry(10,y+10+70*i,100,25)
            self.result[i][1].setGeometry(130,y+70*i,100,50)
            self.result[i][2].setGeometry(210,y+10+70*i,30,25)
            self.result[i][3].setGeometry(240,y+70*i,100,50)
            self.result[i][4].setGeometry(350,y+10+70*i,50,25)
            self.result[i][5].setGeometry(410,y+10+70*i,100,25)
            self.result[i][6].setGeometry(520,y+10+70*i,50,25)
        self.showsearchresultframe.setVisible(False)


    def showairplane(self,data):
        for i in range(1,len(data)+1):
            message = data[i-1].getairplanemessage()
            self.takeoffcity.setText(message[2])
            self.arrivecity.setText(message[3])
            time1 = message[-4][:10]+"\n  "+message[-4][11:]+"\n"+message[4]
            time2 = message[-3][:10]+"\n  "+message[-3][11:]+"\n"+message[5]
            for j in range(7):
                self.result[i][j].setVisible(True)
            self.result[i][0].setText(str(message[0]))
            self.result[i][1].setText(time1)
            self.result[i][3].setText(time2)
            self.result[i][4].setText(str(message[1]))
            self.result[i][5].setText(str(message[-2]))
        for i in range(len(data)+1,10):
            for j in range(7):
                self.result[i][j].setVisible(False)
    def Search(self):
        #self.setoutlineedit self.deslineedit self.setouttime self.returntime  self.pricelineedit  price= or airplanenumber= or offcity = and arrivecity or takeofftime= and arrivetime
        if self.setoutlineedit.text()=="" or self.deslineedit.text()=="" or self.setouttime=="":
            QMessageBox.information(self,"提示","请把搜索内容填完整！")
            return
        airplane1 = []
        airplane3 = []
        if self.pricelineedit.text()!="":
            airplane1 = self.DataBase.findairplane(price=int(self.pricelineedit.text()))#价格不超过指定金额的飞机
        airplane2 = self.DataBase.findairplane(offcity = self.setoutlineedit.text(),arrivecity=self.deslineedit.text()) #起飞城市，抵达城市
        if self.returntime.text()!="":
            airplane3 = self.DataBase.findairplane(returntime = self.returntime.text())#返回时间
        airplane4 = self.DataBase.findairplane(takeofftime=self.setouttime.text(),arrivetime="all")#起飞时间
        print(airplane4)
        correspond =[]
        correspond3 = []
        for airplane in airplane2:
            if airplane in airplane4:
                correspond.append(airplane)
        for i in range(len(correspond)):
            if self.pricelineedit.text()!="":
                if correspond[i] not in airplane1:
                    correspond[i]=None
            if self.returntime.text()!="":
                if correspond[i] not in airplane3:
                    correspond[i]=None
        for a in correspond:
            if a !=None:
                correspond3.append(a)
        if correspond3 ==[]:
            QMessageBox.information(self,"搜索结果","没有符合条件的航班")
            return
        else:
            QMessageBox.information(self, "提示", "搜索成功")
            self.setoutlineedit.setText("")
            self.deslineedit.setText("")
            self.setouttime.setText("")
            self.returntime.setText("")
            self.pricelineedit.setText("")
            self.showairplane(correspond3)
        self.searchframe.setVisible(False)
        self.showsearchresultframe.setVisible(True)
    def Show(self):
        if self.radio1.isChecked():
            self.searchframe.setVisible(True)
            self.administrator.setVisible(False)
        else:
            self.administrator.setVisible(True)
            self.searchframe.setVisible(False)
    def SaveFlight(self):
        #self.input    number,price,amount,offcity,arrivecity,off,destination,time1,time2
        for i in range(10):
            if self.inputs[i][0].text()!="":
                self.DataBase.addairplane(self.inputs[i][0].text(),
                                          self.inputs[i][1].text(),
                                          self.inputs[i][2].text(),
                                          self.inputs[i][3].text(),
                                          self.inputs[i][4].text(),
                                          self.inputs[i][5].text(),
                                          self.inputs[i][6].text(),
                                          self.inputs[i][7].text(),
                                          self.inputs[i][8].text(),
                                          self.inputs[i][9].text()
                                          )
        QMessageBox.information(self,"Success","录入航班信息成功")
    def CheckPassenger(self):
        message = self.DataBase.getusermessage(int(self.checkcustomer.text()),"用户")
        if message == False:
            QMessageBox.information(self,"提示","该客户不存在")
        else :
            for i in range(4):
                self.customerinfor[i].setText(str(message[i+1]))
        print(message)

    def addFlight(self):
        self.administrator = QTabWidget(self)
        self.administrator.setVisible(False)
        self.administrator.setGeometry(50,100,1220,450)
        qwidget1 = QWidget()#航班信息录入
        qwidget2 = QWidget()#客户资料查询
        self.addFlightframe = QFrame(qwidget1)
        self.addFlightframe.setGeometry(10,10,1200,400)
        title = "航班号，票价，可售票数，起飞城市，抵达城市，起飞机场，抵达机场，起飞时间，抵达时间，返回时间".split("，")
        labels = [QLabel(title[i],self.addFlightframe) for i in range(len(title))]
        self.inputs = [[QLineEdit(self.addFlightframe) for i in range(len(title))] for j in range(10)]
        self.savebutton = QPushButton("录入",self.addFlightframe)
        self.savebutton.setGeometry(500,300,80,25)
        self.savebutton.clicked.connect(self.SaveFlight)
        for label in labels:
            label.setFont(QFont("微软雅黑",10,QFont.Bold))
            label.setFrameShape(QFrame.Box)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color:rgb(0,255,255,60)")
        for i in range(len(title)):
            labels[i].setGeometry(120*i,0,120,25)
        for i in range(10):
            for j in range(len(title)):
                self.inputs[i][j].setGeometry(120*j,25*(i+1),120,25)
                self.inputs[i][j].setAlignment(Qt.AlignCenter)
                self.inputs[i][j].setStyleSheet("background-color:rgb(211,211,211,)")
        self.administrator.addTab(qwidget2,"客户资料查询")
        self.administrator.addTab(qwidget1,"航班信息录入")
        frame = QFrame(qwidget2)
        self.checkcustomer = QLineEdit(frame)
        self.checkcustomer.setPlaceholderText("请输入查询的手机号码")
        self.checkcustomer.setAlignment(Qt.AlignCenter)
        self.checkbutton = QPushButton(frame)
        self.checkbutton.setToolTip("查询")
        self.checkbutton.clicked.connect(self.CheckPassenger)
        frame.setGeometry(300,100,400,600)
        self.checkcustomer.setGeometry(25,20,200,25)
        self.checkbutton.setGeometry(250,12,40,40)
        self.checkbutton.setIcon(QIcon("find.jpg"))
        title1 = ["姓名","电话","身份证号","邮箱地址"]
        showmessage = [QLabel(title1[i],frame) for i in range(4)]
        self.customerinfor = [QLabel("******",frame) for i in range(4)]
        for i in range(4):
            showmessage[i].setFont(QFont("微软雅黑",10,QFont.Bold))
            showmessage[i].setGeometry(20,100+40*i,80,45)
            self.customerinfor[i].setGeometry(120,100+40*i,80,45)
    def initUI(self):
        self.resize(1500, 900)
        self.setWindowTitle("飞机订票")
        self.setWindowIcon(QIcon("n.jpg"))
    def CheckAirplane(self):
        self.setoutlabel = QLabel("出发城市")
        self.destinationlabel = QLabel("到达城市")
        self.setoutdate = QLabel("出发日期")
        self.returndate = QLabel("返回日期")
        self.pricelabel = QLabel("最高票价")
        self.setoutlineedit = QLineEdit()
        self.setoutlineedit.setStyleSheet("background-color:rgb(230,230,250,25)")
        self.deslineedit = QLineEdit()
        self.deslineedit.setStyleSheet("background-color:rgb(230,230,250,25)")
        self.setouttime = QLineEdit()
        self.setouttime.setPlaceholderText("yyyy/mm/dd")
        self.setouttime.setStyleSheet("background-color:rgb(230,230,250,25)")
        self.returntime = QLineEdit()
        self.returntime.setPlaceholderText("可不填")
        self.returntime.setStyleSheet("background-color:rgb(230,230,250,25)")
        self.pricelineedit = QLineEdit()
        self.pricelineedit.setPlaceholderText("可不填")
        self.pricelineedit.setStyleSheet("background-color:rgb(230,230,250,25)")
        self.searchframe = QFrame(self)
        #self.searchframe.setStyleSheet("background-color:rgb(0,255,0,25)")
        groupbox = QGroupBox("航班信息查询",self.searchframe)
        self.searchbutton = QPushButton("搜索",self.searchframe)
        self.searchbutton.clicked.connect(self.Search)
        self.searchbutton.setGeometry(100,195,50,25)
        h = [QHBoxLayout() for i in range(5)]
        h[0].addWidget(self.setoutlabel)
        h[0].addWidget(self.setoutlineedit)
        h[1].addWidget(self.destinationlabel)
        h[1].addWidget(self.deslineedit)
        h[2].addWidget(self.setoutdate)
        h[2].addWidget(self.setouttime)
        h[3].addWidget(self.returndate)
        h[3].addWidget(self.returntime)
        h[4].addWidget(self.pricelabel)
        h[4].addWidget(self.pricelineedit)
        v = QVBoxLayout()
        for t in h:
            v.addLayout(t)
        groupbox.setLayout(v)
        self.searchframe.setGeometry(500,300,280,220)
        self.searchframe.setVisible(False)
    def Lognin(self):
        self.frame = QFrame(self)
        #frame.setStyleSheet("background-color:white")
        self.lognbutton = QPushButton("登录")
        self.lognbutton.setEnabled(False)
        self.lognbutton.clicked.connect(self.CheckAccount)
        button = QPushButton("注册")
        button.clicked.connect(self.Register)
        # button.setEnabled(False)
        label = QLabel("手机号码：")
        label2 = QLabel("登录密码：")
        self.tel = QLineEdit()
        self.tel.setPlaceholderText("11位手机号码")
        self.password = QLineEdit()
        self.password.setPlaceholderText("请输入密码")
        self.password.setEchoMode(QLineEdit.Password)
        self.tel.textChanged.connect(self.CheckPassWord)
        self.password.textChanged.connect(self.CheckRegister)
        self.radio1 = QRadioButton("用户登录")
        self.radio2 = QRadioButton("管理员登录")
        self.radio1.setChecked(True)
        hlayout0 = QHBoxLayout()
        hlayout0.addStretch(1)
        hlayout0.addWidget(self.radio1)
        hlayout0.addWidget(self.radio2)
        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(self.tel)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(label2)
        hlayout2.addWidget(self.password)
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.lognbutton)
        hlayout3.addWidget(button)
        vlayout = QVBoxLayout(self.frame)
        vlayout.addStretch(3)
        vlayout.addLayout(hlayout)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(hlayout0)
        vlayout.addLayout(hlayout3)
        self.frame.setGeometry(625,200,250,250)
        self.successframe = QFrame(self)
        self.successframe.setGeometry(1320, 0, 200, 200)
        #self.successframe.setStyleSheet("background-color:white")
        #self.frame.setVisible(False)
        self.successframe.setVisible(False)
        self.welcomelabel = QLabel("欢迎",self.successframe)
        self.avatorlabel = QLabel(self.successframe)
        self.nichenlabel = QLabel("昵称")
        self.changemessage = QPushButton("修改资料",self.successframe)
        self.changemessage.clicked.connect(self.ChangeMessage)
        self.checkticket = QPushButton("已订机票",self.successframe)
        self.quit = QPushButton("退出登录",self.successframe)
        self.welcomelabel.setGeometry(55,0,50,25)
        self.avatorlabel.setGeometry(55,25,60,60)
        self.changemessage.setGeometry(50,90,80,25)
        self.quit.setGeometry(50,125,80,25)
        self.checkticket.setGeometry(50,160,80,25)
        self.checkticket.clicked.connect(self.ReturnTicket)
        self.quit.clicked.connect(self.ChangeRS)
    def ReturnTicket(self):
        print("hahah")
        a = CheckTicket.Checkticket(self.usertel,self.DataBase,self.result)
        print("-"*100)
        a.exec_()
        print("hahahh")
    def ChangeRS(self):
        self.searchframe.setVisible(False)
        self.administrator.setVisible(False)
        if self.successframe.isVisible():
            self.successframe.setVisible(False)
            self.frame.setVisible(True)
            self.showsearchresultframe.setVisible(False)
        else:
            self.successframe.setVisible(True)
            self.frame.setVisible(False)
    def CheckAccount(self):
        passengerstels = self.DataBase.getallpassengertel()
        administratorstel = self.DataBase.getalladministratortel()
        self.usertype = None
        self.usertel = None
        self.userpassword = int(self.password.text())
        if self.radio1.isChecked():
            self.usertype = "用户"
            if int(self.tel.text()) not in passengerstels:
                QMessageBox.warning(self,"错误","该用户不存在")
                return
            else:
                message = self.DataBase.getpassengerpassword(int(self.tel.text()))
                if message[0] != int(self.password.text()):
                    QMessageBox.information(self, "登录失败", "账号或密码输入错误")
                else:
                    QMessageBox.information(self, "登录成功", "欢迎您！" + message[-1]+"用户")
                    self.checkticket.setVisible(True)
                    self.usertel = int(self.tel.text())
                    self.frame.setVisible(False)
                    self.ChangeRS()
                    self.tel.setText("")
                    self.password.setText("")
                    message1 = self.DataBase.getusermessage(self.usertel, self.usertype)
                    self.avatorlabel.setPixmap(QPixmap(message1[-1]))
                    self.Show()
        else:

            self.usertype = "管理员"
            print(administratorstel)
            if int(self.tel.text()) not in administratorstel:
                QMessageBox.warning(self,"错误","该管理员不存在")
                return
            else:
                message = self.DataBase.getadministratorpassword(int(self.tel.text()))
                print("出错啦")
                if message[0] != int(self.password.text()):
                    QMessageBox.information(self, "登录失败", "账号或密码输入错误")
                else:
                    QMessageBox.information(self, "登录成功", "欢迎您！" + message[-1]+"管理员")
                    self.usertel = int(self.tel.text())
                    self.frame.setVisible(False)
                    self.ChangeRS()
                    self.tel.setText("")
                    self.password.setText("")
                    message1 = self.DataBase.getusermessage(self.usertel, self.usertype)
                    self.checkticket.setVisible(False)
                    print(message1)
                    print("ahahahahaha")
                    self.avatorlabel.setPixmap(QPixmap(message1[-1]))
                    for i in range(4):
                        self.customerinfor[i].setText("* * * *")
                    self.checkcustomer.setText("")

                    self.Show()
            message1 = self.DataBase.getusermessage(self.usertel,self.usertype)
            print(message1)
            print("ahahahahaha")
            self.avatorlabel.setPixmap(QPixmap(message1[-1]))
    def CheckPassWord(self):
        if len(self.tel.text())<11:
            return
        self.password.setText("")
        #检查用户是否已经注册
        tels = self.DataBase.getallpassengertel()
        tel2 = self.DataBase.getalladministratortel()
        print(tels)
        print(tel2)
        if int(self.tel.text()) not in tels and int(self.tel.text()) not in tel2:
            result=QMessageBox.question(self,"提示","该账号还没有注册，立即注册？")
            print(result)
            if result == QMessageBox.Yes:
                self.Register()
    def CheckRegister(self):
        if self.password.text()!="" and self.tel.text()!="" and len(self.tel.text())==11:
            self.lognbutton.setEnabled(True)
        else:
            self.lognbutton.setEnabled(False)
    def Event1(self):
        pass
    def Register(self):
        message = []
        a = register.Register(message)
        a.exec_()
        print(message)
        if message==[]:
            return
        if message[-1]=="用户":
            self.DataBase.addpassenger(message[0],message[1],message[2],int(message[3]),int(message[4]),int(message[5]),message[6])
        else:
            self.DataBase.addadministrator(message[0],message[1],message[2],int(message[3]),int(message[4]),int(message[5]),message[6])
    def ChangeMessage(self):
        #QMessageBox.information(self, "提示", "修改成功")

        message = list(self.DataBase.getusermessage(self.usertel,self.usertype))
        message.append(self.userpassword)
        a = revise.Revise(message)
        a.exec_()
        print(message)
        if message[-1]==True:
            if self.usertype =="用户":
                self.DataBase.revisepassengermessage(message[3],message[-3],message[0],message[1],message[2],message[-2],message[3],message[4])
            else:
                self.DataBase.reviseadministratormessage(message[3],message[-3],message[0],message[1],message[2],message[-2],message[3],message[4])
            self.avatorlabel.setPixmap(QPixmap(message[-3]))
    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = QPixmap("607.jpg")
        painter.setOpacity(0.60)
        painter.drawPixmap(self.rect(),pixmap)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())