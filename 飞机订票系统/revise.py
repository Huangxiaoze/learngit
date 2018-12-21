import sys
from PyQt5.QtGui import  QPainter, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, \
    QApplication
import random
class Revise(QDialog):
    def __init__(self,message):
        super().__init__()
        self.message = message
        self.initUI()
        self.setRevise()
    def setRevise(self):
        self.avatorlabel.setPixmap(QPixmap(self.message[-2]))
        for i in range(3):
            self.lineedits[i].setText(str(self.message[i]))
        self.lineedits[-3].setText(str(self.message[3]))
        self.lineedits[-2].setText(str(self.message[4]))
    def showpassword(self):
        self.passwordframe.setVisible(True)
    def changeavatorfunc(self):
        avator = "C:/Users/Hasee/PycharmProjects/image/" + str(random.choice([i for i in range(1, 10)])) + ".jpg"
        self.message[-2]=avator
        self.avatorlabel.setPixmap(QPixmap(avator))
    def initUI(self):
        self.setWindowTitle("修改资料")
        self.setWindowIcon(QIcon("registerimage.jpg"))
        self.setFixedSize(350,450)
        self.avator = QLabel("头像:    ",self)
        self.avator.setGeometry(73,60,50,50)
        self.avatorlabel = QLabel(self)
        self.avatorlabel.setGeometry(153,40,80,80)
        self.avatorlabel.setPixmap(QPixmap("C:/Users/Hasee/PycharmProjects/image/"+str(random.choice([i for i in range(1,10)]))+".jpg"))
        label =["昵称:    ","姓名:    ","电话:    ","旧密码:  ","新密码:  ","身份证号:","邮箱地址:","确认密码:"]
        self.lineedits = [QLineEdit() for i in range(8)]
        for i in range(7):
            self.lineedits[i].setStyleSheet("background-color:white")
        frame = QFrame(self)
        hlayouts = [QHBoxLayout() for i in range(8)]
        labels = [QLabel(label[i]) for i in range(8)]
        for i in range(7):
            hlayouts[i].addWidget(labels[i])
            hlayouts[i].addWidget(self.lineedits[i])
        vlayout = QVBoxLayout(frame)
        vlayout.addStretch(1)
        for i in range(7):
            if i ==3 or i==4 :
                continue
            vlayout.addLayout(hlayouts[i])
        self.passwordframe = QFrame(self)
        self.passwordframe.setGeometry(65,265,250,100)
        self.passwordframe.setVisible(False)
        frame.setGeometry(65,80,250,200)
        hlayouts[-1].addWidget(labels[-1])
        hlayouts[-1].addWidget(self.lineedits[-1])
        self.lineedits[-1].setEchoMode(QLineEdit.Password)
        self.lineedits[-1].textChanged.connect(self.check)
        v = QVBoxLayout(self.passwordframe)
        v.addStretch(1)
        v.addLayout(hlayouts[3])
        v.addLayout(hlayouts[4])
        v.addLayout(hlayouts[-1])
        self.lineedits[3].setEchoMode(QLineEdit.Password)
        self.lineedits[4].setEchoMode(QLineEdit.Password)
        self.button = QPushButton("确认修改",self)
        self.button.clicked.connect(self.changemessage)
        self.button.setGeometry(50,400,90,25)
        self.changeavator = QPushButton("更改",self)
        self.showpasswordframe = QPushButton("修改密码",self)
        self.showpasswordframe.setGeometry(165,400,90,25)
        self.changeavator.setGeometry(240,60,50,30)
        self.showpasswordframe.clicked.connect(self.showpassword)
        self.changeavator.clicked.connect(self.changeavatorfunc)
    def changemessage(self):
        print(self.lineedits[3].text())

        if self.lineedits[3].text()!="" and self.lineedits[3].text()!=str(self.message[-1]):
            QMessageBox.warning(self,"error","旧密码错误")
            return
        QMessageBox.information(self,"Information","修改成功")
        self.message[0] = self.lineedits[0].text()
        self.message[1]=self.lineedits[1].text()
        self.message[2] = int(self.lineedits[2].text())
        self.message[3]= int(self.lineedits[-3].text())
        self.message[4] = self.lineedits[-2].text()
        if self.lineedits[-1].text()!="":
            self.message[-1] = int(self.lineedits[-1].text())
        print(self.message)
        self.message.append(True)
        self.close()
    def check(self):
        print("hahha")
        if self.lineedits[4].text()!="" and len(self.lineedits[4].text()) == len(self.lineedits[-1].text()):
            if self.lineedits[-1].text()!= self.lineedits[4].text():
                QMessageBox.warning(self,"Warning","新密码不一致")
    def getmessage(self):
        l = []
        for i in range(7):
            l.append(self.lineedits[i].text())
        return l
    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = QPixmap("airplane.jpg")
        painter.setOpacity(0.8)#设置不透明度
        painter.drawPixmap(self.rect(),pixmap)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    message = ['黄小泽', '黄泽文', 15768497448, 440982199801283458, '1317670668@qq.com', 'C:/Users/Hasee/PycharmProjects/image/8.jpg', 1228]
    w = Revise(message)
    w.show()
    print(message)
    sys.exit(app.exec_())
