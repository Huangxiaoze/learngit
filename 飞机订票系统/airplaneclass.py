from copy import copy
class Ticket:
    def __init__(self):
        self.nextticket = None
    def setticket(self,number,price,offcity,arrivecity,off,destination,time1,time2):
        self.offcity = offcity
        self.arrivecity = arrivecity
        self.takeoffairport = off
        self.destination = destination
        self.takeofftime = time1
        self.arrivetime = time2
        self.price = price
        self.airplanenumber = number
    def getticketmessage(self):
        return self.airplanenumber,self.price,self.offcity,self.arrivecity,self.takeoffairport,self.destination,self.takeofftime,self.arrivetime
class Message:
    def setmessage(self,avator,nichen,name,tel,password,identify,email):
        self.nichen = nichen
        self.name = name
        self.tel = tel
        self.password = password
        self.identify = identify
        self.email =email
        self.avator = avator
    def getmessage(self):
        return self.nichen,self.name,self.tel,self.identify,self.email,self.avator
class Passenger:
    def __init__(self):
        self.tickets = None
        self.message = Message()
        self.nextpassenger = None
class Administrator:
    def __init__(self):
        self.message = Message()
        self.nextadministrator = None
class Airplane:
    def __init__(self):
        self.nextairplane = None
        self.ticket = Ticket()
    def setariplane(self,number,price,amount,offcity,arrivecity,off,destination,time1,time2,time3):
        self.ticket.setticket(number,price,offcity,arrivecity,off,destination,time1,time2)
        self.offcity = offcity
        self.arrivecity = arrivecity
        self.takeoffairport = off
        self.destination = destination
        self.takeofftime = time1
        self.arrivetime = time2
        self.price = price
        self.airplanenumber = number
        self.amount = amount
        self.returntime = time3
    def getairplanemessage(self):
        return self.airplanenumber,self.price,self.offcity,self.arrivecity,self.takeoffairport,self.destination,self.takeofftime,self.arrivetime,self.amount,self.returntime
class AirlineCompany:
    def __init__(self):
        self.airplanes = None
        self.administrators = None
        self.passengers = None

    def getpassengerticket(self,tel):
        print("getpassengerticket")
        p = self.passengers
        while p.message.tel!=tel:
            p = p.nextpassenger
        tickets = []
        ticket = p.tickets
        i = 0
        while ticket!=None:
            i+=1
            print(i)
            tickets.append(ticket.getticketmessage())
            ticket = ticket.nextticket
        print("over")
        return tickets

    def addairplane(self,*airplanemessage):
        #增加航班
        print(airplanemessage)
        airplane = Airplane()
        airplane.setariplane(airplanemessage[0],airplanemessage[1],airplanemessage[2],airplanemessage[3],
                             airplanemessage[4],airplanemessage[5],airplanemessage[6],airplanemessage[7],airplanemessage[8],airplanemessage[9])
        a = self.airplanes
        if a == None:
            self.airplanes = airplane
        else:
            while a.nextairplane!=None:
                a = a.nextairplane
            a.nextairplane = airplane
    def findairplane(self,**targetobject):
        print(targetobject)
        #获取符合条件的所有飞机 price= or airplanenumber= or offcity = and arrivecity or takeofftime= and arrivetime or returntime
        correspond = []
        a = self.airplanes
        if len(targetobject)==1:
            key,value = targetobject.popitem()
            if key == "airplanenumber":
                while a!=None:
                    if a.airplanenumber == value:
                        correspond.append(a)
                    a = a.nextairplane
            elif key == "price":
                while a!=None:
                    if a.price <= value:
                        correspond.append(a)
                    a = a.nextairplane
            elif key =="returntime":
                print(key,value)
                while a!=None:
                    if a.returntime == value:
                        correspond.append(a)
                    a = a.nextairplane
        else:
            if  "offcity" in targetobject.keys():
                while a!=None:
                    if a.offcity==targetobject["offcity"] and a.arrivecity==targetobject["arrivecity"]:
                        correspond.append(a)
                    a = a.nextairplane
            elif targetobject["arrivetime"]!="all":
                while a!=None:
                    if targetobject["takeofftime"] in a.takeofftime and  targetobject["arrivetime"] in a.arrivetime:
                        correspond.append(a)
                    a = a.nextairplane
            else:
                while a!=None:
                    if targetobject["takeofftime"] in a.takeofftime:
                        correspond.append(a)
                    a = a.nextairplane
        return correspond
    def addadministrator(self,*message):
        #管理员注册时调用
        administrator = Administrator()
        administrator.message.setmessage(message[0],message[1],message[2],message[3],message[4],message[5],message[6])
        a = self.administrators
        if a == None:
            self.administrators = administrator
        else:
            while a.nextadministrator != None:
                a = a.nextadministrator
            a.nextadministrator = administrator
    def addpassenger(self,*message):
        #用户注册时调用
        passenger = Passenger()
        passenger.message.setmessage(message[0],message[1],message[2],message[3],message[4],message[5],message[6])
        p = self.passengers
        if p ==None:
            self.passengers = passenger
        else:
            while p.nextpassenger!=None:
                p = p.nextpassenger
            p.nextpassenger = passenger
    def revisepassengermessage(self,identify,*message):
        print(message)
        print("hahahah")
        #用户修改资料时调用
        p = self.passengers
        while p.message.identify != identify:
            p = p.nextpassenger
        p.message.setmessage(message[0],message[1],message[2],message[3],message[4],message[5],message[6])
    def reviseadministratormessage(self,identify,*message):
        # 管理员修改资料时调用
        p = self.administrators
        while p.message.identify != identify:
            p = p.nextadministrator
        p.message.setmessage(message[0], message[1], message[2], message[3], message[4], message[5], message[6])
    def getusermessage(self,tel,type):
        #查找用户信息时调用
        print("getusermessage")
        if type == "用户":
            p = self.passengers
            tag = False
            while True:
                if p ==None:
                    break
                if p.message.tel == tel:
                    tag =True
                    break
                p = p.nextpassenger
            if tag == False:
                return False
            return p.message.getmessage()
        else:
            p = self.administrators
            tag = False
            while True:
                if p == None:
                    break
                if p.message.tel == tel:
                    tag = True
                    break
                p = p.nextadministrator
            if tag == False:
                return False
            return p.message.getmessage()
    def getallpassengertel(self):
        #获得所有客户的电话
        tels = []
        p = self.passengers
        while p!=None:
            tels.append(p.message.tel)
            p = p.nextpassenger
        return tels
    def getalladministratortel(self):
        #获得所有管理员的电话
        print("hello")
        tels =[]
        a = self.administrators
        while a!=None:
            tels.append(a.message.tel)
            a = a.nextadministrator
        return tels

    def booking(self,tel,airplanenumber,takeofftime,arrivetime):
        #订票
        print("booking..........")
        print(tel,airplanenumber,takeofftime,arrivetime)
        a = self.airplanes
        while a!=None:
            if a.airplanenumber == airplanenumber and a.takeofftime==takeofftime and a.arrivetime==arrivetime:
                break
            a = a.nextairplane
        if a.amount == 0:
            return False
        p = self.passengers
        while p!=None:
            if p.message.tel == tel:
                ticket = copy(a.ticket)
                if p.tickets==None:
                    p.tickets = ticket
                else:
                    t = p.tickets
                    while t.nextticket!=None:
                        t = t.nextticket
                    t.nextticket = ticket
                b = a
                a.amount-=1
                self.printallairplaneticket()
                print(a.amount,b.amount)
                return True
            p = p.nextpassenger
    def printallairplaneticket(self):
        a = self.airplanes
        while a.nextairplane!=None:
            print(a.airplanenumber,a.amount)
            a = a.nextairplane
    def return_a_ticket(self,identify,No,airplanenumber):
        #退票
        a = self.airplanes
        p = self.passengers
        while p.message.identify!= identify:
            p = p.nextpassenger
        formerticket = p.tickets
        latterticket = p.tickets
        if No ==0:
            p.tickets = None
        else:
            for i in range(No-1):
                formerticket = formerticket.nextticket
            for i in range(No+1):
                latterticket = latterticket.nextticket
            formerticket.nextticket = latterticket
        while a.airplanenumber!=airplanenumber:
            a = a.nextairplane
        a.amount+=1
        self.printallairplaneticket()
        print(a.amount,airplanenumber)
    def getadministratorpassword(self,tel):
        #获得管理员登录密码
        print("getadministratorpassword")
        p = self.administrators
        while p.message.tel != tel:
            p = p.nextadministrator
        print("getpassengerword")
        return p.message.password, p.message.name
    def getpassengerpassword(self,tel):
        #获得用户登录密码
        p = self.passengers
        while p.message.tel!= tel:
            p = p.nextpassenger
        print("getpassengerword")
        return p.message.password,p.message.name



if __name__ == '__main__':

    airplanecompany = AirlineCompany()
    airplanecompany.addpassenger("C:/Users/Hasee/PycharmProjects/image/8.jpg", "黄小泽", "黄泽文", 15768497440, 1228, 44098,
                               "1317670668@qq.com")
    airplanecompany.addadministrator("C:/Users/Hasee/PycharmProjects/image/7.jpg", "黄小红", "黄小红", 15363159240, 1228, 12,
                                   12)
    airplanecompany.addairplane(101, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00",
                              "2018/12/25/18:00")
    airplanecompany.addairplane(102, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/20/19:00", "2018/12/22/19:00",
                              "2018/12/24/19:00")
    airplanecompany.addairplane(104, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/20/18:00", "2018/12/22/18:00",
                              "2018/12/23/18:00")
    airplanecompany.addairplane(102, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/21/19:00", "2018/12/22", "2018/12/23")
    airplanecompany.addairplane(101, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/22", "2018/12/22", "2018/12/25")
    airplanecompany.addairplane(102, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/22", "2018/12/22", "2018/12/24")
    airplanecompany.addairplane(101, 100, 11, "深圳", "上海", "机场1", "机场2", "2018/12/23", "2018/12/22", "2018/12/25")
    airplanecompany.addairplane(102, 110, 11, "广州", "上海", "机场1", "机场2", "2018/12/23", "2018/12/22", "2018/12/24")
    airplanecompany.booking(15768497440,101,"2018/12/20/18:00", "2018/12/22/18:00")

    #airplanes = airplanecompany.findairplane(offcity="深圳",arrivecity="上海")
    airplanes = airplanecompany.findairplane(takeofftime="1",arrivetime="2")
    for airplane in airplanes:
        print(airplane.getairplanemessage())
    #,number,price,amount,offcity,arrivecity,off,destination,time1,time2
    print(airplanecompany.getallpassengertel())