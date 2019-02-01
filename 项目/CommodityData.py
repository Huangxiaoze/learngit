import datetime
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableView
class Commodity(QTableView):
    def __init__(self):
        super().__init__()
        self.db = None
        self.db_connect()
        self.CreateTable()
        self.sql_exec()
    def db_connect(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')  # 1
        self.db.setDatabaseName('./tes.db')  # 2
        if not self.db.open():  # 3
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())
    def closeEvent(self, QCloseEvent):  # 4
        self.db.close()
    def CreateTable(self):
        query = QSqlQuery()
        query.exec_("create table yingyee(date VARCHAR(20) primary key,name VARCHAR(20),total VARCHAR(20),status VARCHAR(20))")
        query.exec_("CREATE TABLE sh(number VARCHAR(20) PRIMARY KEY, name VARCHAR(20) NOT NULL, unit VARCHAR(20))")
        s=""
        for i in range(1,11):
            s+="No{0} VARCHAR(20),goods{6} VARCHAR(20),unit{1} VARCHAR(20),guige{2} VARCHAR(20),amount{3} VARCHAR(20),danjia{4} VARCHAR(20),money{7} VARCHAR(20),beizhu{5} VARCHAR(20),".format(i,i,i,i,i,i,i,i)
        print(s)
        query.exec_("CREATE TABLE Kucun("
                    "date VARCHAR(20) primary key,"
                    " name VARCHAR(20) NOT NULL,"
                    " bianhao VARCHAR(20),"
                    "cangku VARCHAR(20),"
                    "tel VARCHAR(20),"
                    "address VARCHAR(20),"
                    "zhidan VARCHAR(20),"
                    "jinshou VARCHAR(20),"
                    "shoukuan VARCHAR(20),"
                    "fahuo VARCHAR(20),"
                    "kehuqianzi VARCHAR(20),"+s+"total VARCHAR(20))")

        """
        query.exec_("insert into Kucun(date,name,bianhao,cangku,tel,address,zhidan,jinshou,shoukuan"
                    ",fahuo,kehuqianzi,No1,goods1,unit1,guige1,amount1,danjia1,money1,beizhu1,total)"
                    "values ({}".format("\'"+datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+"\'")+",'黄小泽','2017151024','20','15768497448','广东',"
                    "'小红','小黄','小兰','小明','小倩','2017','牙膏','根','加工','8','12','96','没有','96.0')")
        
        query.exec_("insert into Kucun(date,name,bianhao) values('2018/11/26 5','黄泽文','2017151024')")
        """
        query.exec_("SELECT            date,name,bianhao,cangku,tel,address,zhidan,jinshou,shoukuan"
                    ",fahuo,kehuqianzi,No1,unit1,guige1,amount1,danjia1,beizhu1 FROM Kucun")  # 4

        while query.next():
            print(query.value(0),query.value(1),query.value(2))



        query.exec_("insert into sh(number,name)"
                    "values ('1023','不锈钢')")
        query.exec_("SELECT number, name FROM sh")  # 4
        while query.next():
            stu_name = query.value(0)
            stu_class = query.value(1)
            print(stu_name, stu_class)
    def SetTable(self,table):
        self.model.setTable(table)
    def sql_exec(self):
        self.model = QSqlTableModel()
        self.model.setTable('sh')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0,Qt.Horizontal,"商品编号")
        self.model.setHeaderData(1,Qt.Horizontal,"商品名称")
        self.model.setHeaderData(2,Qt.Horizontal,"单位")
        self.model.select()
        self.setModel(self.model)
    def InsertData(self,number,name,unit):
        if number =="" or name=="" or unit=="":
            return
        self.model.insertRow(0)
        self.model.setData(self.model.index(0,0),number)
        self.model.setData(self.model.index(0,1),name)
        self.model.setData(self.model.index(0,2),unit)
        self.model.submit()
    def Find(self,number):
        self.model.setFilter('number=='+number)
        self.model.select()
        if self.model.record(0).value("number")==None:
            return False
        return True
    def getData(self,number):
        if self.Find(number):
            record = self.model.record(0)
            l = [record.value("number"),record.value("name"),record.value("unit")]
            return l
        else:
            return None
    def UpDate(self,number,type,data):
        dic = {"number":0,"name":1,"unit":2}
        if self.Find(number):
            self.model.setData(self.model.index(0,dic[type]),data)
            return True
        return False


"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Commodity()
    #demo.InsertData("3014","铁","箱")
    #print(demo.Find("104"))
    #print(demo.getData("2014"))
    #demo.UpDate("2014","name","木棍")
    demo.show()

    sys.exit(app.exec_())
"""