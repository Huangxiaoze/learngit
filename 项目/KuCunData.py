import sys
import datetime
import CommodityData
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableView
class KuCunDan(QTableView):
    def __init__(self,commodity):
        super().__init__()
        self.db = None
        self.commodity = commodity
        self.sql_exec()
    def sql_exec(self):
        self.commodity.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.commodity.model.setHeaderData(0,Qt.Horizontal,"日期")
        self.commodity.model.setHeaderData(1,Qt.Horizontal,"客户")
        self.commodity.model.setHeaderData(2,Qt.Horizontal,"编号")
        self.commodity.model.setHeaderData(3, Qt.Horizontal, "出货仓库")
        self.commodity.model.setHeaderData(4, Qt.Horizontal, "客户电话")
        self.commodity.model.setHeaderData(5, Qt.Horizontal, "地址")
        self.commodity.model.setHeaderData(6, Qt.Horizontal, "制单人")
        self.commodity.model.setHeaderData(7, Qt.Horizontal, "经手人")
        self.commodity.model.setHeaderData(8, Qt.Horizontal, "收款人")
        self.commodity.model.setHeaderData(9, Qt.Horizontal, "发货人")
        self.commodity.model.setHeaderData(10, Qt.Horizontal, "客户签字")
        j=10
        for i in range(1,11):
            self.commodity.model.setHeaderData(j+1, Qt.Horizontal, "No.{}".format(i))
            self.commodity.model.setHeaderData(j+2,Qt.Horizontal,"商品名称{}".format(i))
            self.commodity.model.setHeaderData(j+3, Qt.Horizontal, "单位{}".format(i))
            self.commodity.model.setHeaderData(j+4, Qt.Horizontal, "规格{}".format(i))
            self.commodity.model.setHeaderData(j+5, Qt.Horizontal, "数量{}".format(i))
            self.commodity.model.setHeaderData(j+6, Qt.Horizontal, "单价{}".format(i))
            self.commodity.model.setHeaderData(j+7,Qt.Horizontal,"金额{}".format(i))
            self.commodity.model.setHeaderData(j+8, Qt.Horizontal, "备注{}".format(i))
            j=j+8
        self.commodity.model.select()
        self.setModel(self.commodity.model)
    def InsertData(self,data):
        nowtable = self.commodity.model.tableName()
        if len(data)==0 :
            return
        print("插入库存")
        self.commodity.model.setTable("Kucun")
        self.commodity.model.select()

        self.commodity.model.insertRow(0)
        for i in range(91):
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
                l = [record.value(i) for i in range(91)]
                i+=1
                alldata.append(l)
            return alldata
        else:
            return None
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

    demo = KuCunDan(commodity)
    demo.commodity.model.setTable("Kucun")
    demo.commodity.model.select()
    demo.RemoveData("date","2017","==")
    print(demo.commodity.model.tableName())
    demo.show()

    sys.exit(app.exec_())
"""