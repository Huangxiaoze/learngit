import sys
from PyQt5.QtGui import QPainter, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QDialog, QLabel,  QFrame,  QPushButton, QApplication
class Checkticket(QDialog):
    def __init__(self,usertel,Database,result):
        super().__init__()
        self.result = result
        self.Database = Database
        self.tel = usertel
        message = self.Database.getusermessage(self.tel,"用户")
        self.name = message[1]
        self.id = message[-3]
        self.data = self.Database.getpassengerticket(self.tel)
        self.initUI()
        self.show()
    def ReturnTicket(self,i,j):
        self.Database.return_a_ticket(self.id,i*4+j,self.data[i*4+j][0])
        number = self.data[i*4+j][0]
        for k in range(1,10):
            if self.result[k][0].text()==str(number):
                self.result[k][5].setText(str(int(self.result[k][5].text())+1))
                self.result[k][6].setVisible(True)
                break
        del self.data[i*4+j]
        self.ShowTicket()
    def ShowTicket(self):
        for i in range(2):
            for j in range(4):
                if i*4+j<len(self.data):
                    self.frameworklabels[i][j].setVisible(True)
                    self.buttons[i][j].setVisible(True)
                    time1 = self.data[i][-2][:10]+'\n'+self.data[i][-2][11:]+'\n'+self.data[i][-4]
                    time2 = self.data[i][-1][:10]+'\n'+self.data[i][-1][11:]+'\n'+self.data[i][-3]
                    for k in range(7):
                        self.labels[i][j][k].setVisible(True)
                    self.labels[i][j][0].setText(self.data[i][2])
                    self.labels[i][j][2].setText(self.data[i][3])
                    self.labels[i][j][3].setText(time1)
                    self.labels[i][j][5].setText(time2)
                    self.labels[i][j][6].setText("航班："+str(self.data[i*4+j][0])+"\n票价："+str(self.data[j][1])+"\n姓名："+self.name+"\nID："+str(self.id))
                else:
                    self.frameworklabels[i][j].setVisible(False)
                    self.buttons[i][j].setVisible(False)
                    for k in range(7):
                        self.labels[i][j][k].setVisible(False)
    def initUI(self):
        self.setFixedSize(620,520)
        self.setWindowIcon(QIcon("registerimage.jpg"))
        self.setWindowTitle("已订机票")
        self.frameworklabels = [[QLabel(self) for i in range(4)] for j in range(2)]
        self.buttons = [[QPushButton("退票",self) for i in range(4)] for j in range(2) ]
        self.buttons[0][0].clicked.connect(lambda:self.ReturnTicket(0,0))
        self.buttons[0][1].clicked.connect(lambda: self.ReturnTicket(0,1))
        self.buttons[0][2].clicked.connect(lambda: self.ReturnTicket(0,2))
        self.buttons[0][3].clicked.connect(lambda: self.ReturnTicket(0,3))
        self.buttons[1][0].clicked.connect(lambda: self.ReturnTicket(1,0))
        self.buttons[1][1].clicked.connect(lambda: self.ReturnTicket(1,1))
        self.buttons[1][2].clicked.connect(lambda: self.ReturnTicket(1,2))
        self.buttons[1][3].clicked.connect(lambda: self.ReturnTicket(1,3))
        self.labels = [[[QLabel("城市1",self) for i in range(7) ] for j in range(4)] for z in range(2)]
        for i in range(2):
            for j in range(4):
                for z in range(7):
                    if z ==3 or z == 5:
                        self.labels[i][j][z].setFont(QFont("微软雅黑",6,QFont.Bold))
                    else:
                        self.labels[i][j][z].setFont(QFont("微软雅黑",7,QFont.Bold))
                self.labels[i][j][0].setText("深圳 ")
                self.labels[i][j][1].setText("   →")
                self.labels[i][j][2].setText("上海")
                self.labels[i][j][3].setText("2018/12/20\n09:12\njichang")
                self.labels[i][j][4].setText("→")
                self.labels[i][j][5].setText("2018/12/20\n09:12\njichang")
                self.labels[i][j][6].setText("航班："+str(2)+"\n姓名\nID"+str(i)+str(j))
        x = 10
        y = 10
        for i in range(2):
            for j in range(4):
                self.frameworklabels[i][j].setGeometry(x+150*j,y+260*i,140,200)
                self.labels[i][j][0].setGeometry(x+150*j +10,y+260*i+20,30,20)
                self.labels[i][j][1].setGeometry(x+150*j+30,y+260*i+20,30,20)
                self.labels[i][j][2].setGeometry(x+150*j+60,y+260*i+20,30,20)
                self.labels[i][j][3].setGeometry(x+150*j+10,y+260*i+50,60,50)
                self.labels[i][j][4].setGeometry(x+150*j+65,y+260*i+65,30,30)
                self.labels[i][j][5].setGeometry(x+150*j+80,y+260*i+50,60,50)
                self.labels[i][j][6].setGeometry(x+150*j+10,y+260*i+100,120,90)
                self.frameworklabels[i][j].setFrameShape(QFrame.Box)
                self.buttons[i][j].setGeometry(x+20+150*j,y+210+260*i,40,30)
        self.ShowTicket()
    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = QPixmap("airplane.jpg")
        painter.setOpacity(0.8)#设置不透明度
        painter.drawPixmap(self.rect(),pixmap)
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #number, price, offcity, arrivecity, off, destination, time1, time2
    m=[(101, 100, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00"),(101, 100, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00")]
    w = Register(m,4409,"黄小泽")
    print("hahah")
    w.show()

    sys.exit(app.exec_())"""