import sys
import datetime
import CommodityData
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableView
class YingYeE(QTableView):
    def __init__(self,commodity):
        super().__init__()
        self.db = None
        self.commodity = commodity
        self.sql_exec()
    def sql_exec(self):
        print("hello")
        self.commodity.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.commodity.model.setHeaderData(0,Qt.Horizontal,"日期")
        self.commodity.model.setHeaderData(1,Qt.Horizontal,"客户名称")
        self.commodity.model.setHeaderData(2,Qt.Horizontal,"订单金额")
        self.commodity.model.setHeaderData(3, Qt.Horizontal, "付款状态")
        self.commodity.model.select()
        self.setModel(self.commodity.model)
    def InsertData(self,data):
        nowtable = self.commodity.model.tableName()
        if len(data)==0 or data[0]=="" or data[1]=="" or data[2]=="" or data[3]=="":
            return
        print("插入营业额")
        self.commodity.model.setTable("yingyee")
        self.commodity.model.select()
        self.commodity.model.insertRow(0)
        for i in range(4):
            self.commodity.model.setData(self.commodity.model.index(0,i),data[i])
        self.commodity.model.submit()
        self.commodity.model.setTable(nowtable)
        self.commodity.model.select()

    def Find(self,key,value,compare):
        self.commodity.model.setFilter('{0}{1}\''.format(key,compare)+'{}\''.format(value))
        #self.model.setFilter('date==\'2018/11/25\'')
        self.commodity.model.select()
        if self.commodity.model.record(0).value(key)==None:
            return False
        return True

    def getData(self,key,value,compare):
        alldata =[]
        if self.Find(key,value,compare):
            i =0
            while self.commodity.model.record(i).value(0)!=None:
                record = self.commodity.model.record(i)
                l = [record.value(i) for i in range(4)]
                i+=1
                alldata.append(l)
            return alldata
        else:
            return None
    def ReviseStatus(self,date,status):
        print("修改状态")
        nowtable = self.commodity.model.tableName()
        self.commodity.model.setTable("yingyee")
        if self.Find("date",date,"=="):
            print("yes")
            self.commodity.model.setData(self.commodity.model.index(0,3),status)
            #self.commodity.model.submit()
        self.commodity.model.setTable(nowtable)
        self.commodity.model.select()

    def RemoveData(self,key,value,compare):
        """
        为了确保删除的唯一性
        :param key: 时间
        :param value: 时间
        :param compare: 等于
        :return:
        """
        if self.Find(key,value,compare):
            self.commodity.model.removeRow(0)
            self.commodity.model.submit()
            return True
        return False
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    commodity = CommodityData.Commodity()
    commodity.model.setTable("yingyee")
    demo = YingYeE(commodity)
    demo.commodity.model.select()
    print(demo.commodity.model.tableName())
    #demo.InsertData(["2018/11/23","黄小泽","100.00","已付款"])
    #demo.Find("date","2018/11/26","==")
    #print(demo.getData("name","黄小泽","=="))
    #demo.ReviseStatus("2018/11/28 07:33:52","未付款")
    demo.show()

    sys.exit(app.exec_())
"""