import sys

from PyQt5.QtGui import  QPainter, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, \
    QApplication, QComboBox
import random
class Register(QDialog):
    def __init__(self,message):
        super().__init__()
        self.message = message
        self.initUI()
    def initUI(self):
        self.setWindowTitle("用户注册")
        self.setWindowIcon(QIcon("registerimage.jpg"))
        self.setFixedSize(350,420)
        self.avator = QLabel("头像:    ",self)
        self.avator.setGeometry(73,60,50,50)
        self.avatorlabel = QLabel(self)
        self.avatorlabel.setGeometry(153,40,80,80)
        self.avatorpath = "C:/Users/Hasee/PycharmProjects/image/"+str(random.choice([i for i in range(1,10)]))+".jpg"
        self.avatorlabel.setPixmap(QPixmap(self.avatorpath))
        label =["昵称:    ","姓名:    ","电话:    ","密码:    ","确认密码:","身份证号:","邮箱地址:","注册身份:"]
        self.lineedits = [QLineEdit() for i in range(7)]
        for i in range(7):
            self.lineedits[i].setStyleSheet("background-color:white")
        frame = QFrame(self)
        hlayouts = [QHBoxLayout() for i in range(8)]
        labels = [QLabel(label[i]) for i in range(8)]
        for i in range(7):
            hlayouts[i].addWidget(labels[i])
            hlayouts[i].addWidget(self.lineedits[i])

        self.combobox = QComboBox(self)
        self.combobox.addItem("用户")
        self.combobox.addItem("管理员")
        hlayouts[-1].addWidget(labels[-1])
        hlayouts[-1].addWidget(self.combobox)
        vlayout = QVBoxLayout(frame)
        for i in range(8):
            vlayout.addLayout(hlayouts[i])
        frame.setGeometry(65,125,250,230)
        self.lineedits[3].setEchoMode(QLineEdit.Password)
        self.lineedits[4].setEchoMode(QLineEdit.Password)
        self.lineedits[4].textChanged.connect(self.check)
        self.button = QPushButton("注册",self)
        self.button.clicked.connect(self.register0)
        self.button.setGeometry(140,360,50,25)
    def register0(self):
        tag = True
        for i in range(7):
            if self.lineedits[i].text()=="":
                QMessageBox.information(self,"Information","请把信息填完整")
                return
        QMessageBox.information(self,"Information","注册成功")
        self.getmessage()
        self.close()
    def check(self):
        if self.lineedits[3].text()!="" and len(self.lineedits[3].text()) == len(self.lineedits[4].text()):
            if self.lineedits[3].text()!= self.lineedits[4].text():
                QMessageBox.warning(self,"Warning","密码不一致")
    def getmessage(self):
        self.message.append(self.avatorpath)
        for i in range(7):
            if i !=3:
                self.message.append(self.lineedits[i].text())
        self.message.append(self.combobox.currentText())

    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = QPixmap("airplane.jpg")
        painter.setOpacity(0.8)#设置不透明度
        painter.drawPixmap(self.rect(),pixmap)
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m=[]
    w = Register(m)
    w.show()

    sys.exit(app.exec_())"""