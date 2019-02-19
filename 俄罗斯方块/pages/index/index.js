function rand(min, max) {
  return parseInt((Math.random() * 100) % (max - min) + min)
}
function setParam(){
  state = rand(1, 5)
  First = rand(0, 5)
  FillColor = Color[rand(0,Color.length)]
  BorderColor = Color1[rand(0,Color1.length)]
  console.log(FillColor)
  if (First == 1) {
    var s = rand(0, 1)
    if (s == 0) Second = 0
    else Second = 2
  }
  else if (First == 3) {
    var s = rand(0, 1)
    if (s == 0) Second = 0.5
    else Second = -0.5
  }
  ChangeMax(First)
}
function ChangeMax(first){
  if (First == 0) {
    maxrow = alph[state % 2][0][0]
    maxcol = alph[state % 2][0][1]
  }
  else if (First == 2) {
    maxcol = 2
    maxrow = 2
  }
  else {
    maxrow = alph[state % 2][1][1]
    maxcol = alph[state % 2][1][0]
  }
}
function can_get_score(row){
  var count=0
  for(var i=0;i!=maxh;i++)
    if(GameMap[row][i].canplace==false) count++
  if(count==maxh) return true
  return false
}
function judge(){
  var rowcount=0
  var Y = null
  var Ylabel = true
  for(var i= maxv-1;i>0;i--){
    var count= 0
    var count1 = 0
    for (var j = 0; j != maxh; j++){
      if (GameMap[i][j].canplace == false) count++
      if(GameMap[i-1][j].canplace ==false) count1++
    }
    if(count==maxh) rowcount++
    if(count==maxh&&Ylabel==true){
      Y = i
      Ylabel = false
    }
    if(count1!=maxh&&rowcount!=0){
      Save_destroy.push({
        y:Y,
        count:rowcount
      })
      rowcount=0
      Ylabel = true
    }
    if(count1==0) break
  }
}
function Clear(){
  for(var i=0;i!=Save_destroy.length;i++){
    var length = Save_destroy[i].count
    add+=length
    var max = Save_destroy[i].y*width
    var min = (Save_destroy[i].y-length)*width
    for(var r=0;r!=Save.length;r++)
      for(var j=0;j!=4;j++)
      if(Save[r].points[j].y<=min&&Save[r].points[j].y!=-1)
        Save[r].points[j].y +=width*length
      else if(Save[r].points[j].y<=max&&Save[r].points[j].y>min){
        Save[r].points[j].y=-1
      }
  }


}

var width = 20
var Border=3
var BorderColor ='#8A2BE2'
var FillColor = 'yellow'
var Color = ['#8A2BE2', '#6495ED', '#DC143C','#00FFFF']
var Color1 = ['#8A2BE2', '#6495ED', '#DC143C', '#00FFFF']
var add = 0
var Continue = true
var alph = [
  [
    [1,4],[2,3]
  ],
  [
    [4,1],[3,2]
  ]
]
var maxrow = 0
var maxcol = 0
var First = 0
var Second = 0
var maxh = 0
var maxv = 0
var changestate = false
var counter=-1
var counter2=0
var state=1
var x1=3*width
var y1=0
var xstart =0
var xend=0
var framenum=0
var windowheight=0
var windowwidth=0
var save = false
var Save = []
var Save_destroy = []
var can_not_place=[]
var Point = function(){
    this.x = x1
    this.y= y1
}
var GameMap = []
var pointobj = function(){
    this.points = []
    for(var i=0;i!=4;i++)
    this.points.push(new Point())
  this.fillcolor ="#D2691E"
  this.bordercolor = '#D2691E'
}
var maxLength=[]
setParam()


Page({
  data: {
    height:0,
    width:0,
    mod:30,
    Score:0,
    src: 'https://m10.music.126.net/20190218180112/e69dbcdef1d7513b449c2c053dac920e/ymusic/a24a/fb6c/7fb9/9c864443ebb5efc6160b826c607b9071.mp3'
  },
  changespeed:function(e){
    this.setData({mod:e.detail.value})
  },
  Changestate:function(e){
    if((maxh*width-x1)/width<maxrow||(maxv*width-y1)/width<maxcol) return
    state++
    if(state==5) state=1
    ChangeMax()
    xstart = e.touches[0].x
  },
  MoveLeft:function(e){
    x1-=width
    if(x1<0) x1 = 0
  },
  MoveRight:function(){
    if(x1+maxcol*width==maxh*width) return
    x1+=width
  },
  onLoad:function(){
    this.audio = wx.createInnerAudioContext()
    this.audio.src = this.data.src
    this.audio.autoplay = true
    this.audio.loop = true
    var brush = wx.createCanvasContext('mycanvas')
    brush.setLineCap('round')
    var t1 = function(s,x,y){
      var maxy = -1
      var point = new pointobj()
      point.bordercolor = BorderColor
      point.fillcolor = FillColor
      if(s%2==0){
        for (var i = 0; i != 4; i++){
          point.points[i].x = width*i+x
          point.points[i].y = y
        }
      }
      else{
        for (var i = 0; i != 4; i++){
          point.points[i].x = x
          point.points[i].y=i*width+y
        }
      }
      DrawRect(point)
      brush.stroke()
      return get_point(maxy,point)
    }
    var t2 = function(x,y){
      var maxy = -1
      var point = new pointobj()
      point.bordercolor = BorderColor
      point.fillcolor = FillColor
      var k = 0
      for(var i=0;i!=2;i++)
        for(var j=0;j!=2;j++){
          point.points[k].x = width*j+x
          point.points[k].y = width*i+ y
          k++
        }
      DrawRect(point)
      brush.stroke()
      return get_point(maxy,point)
    }
    var t3 = function(s,x,y,t){
      var maxy = -1
      var point = new pointobj()
      point.bordercolor = BorderColor
      point.fillcolor = FillColor
      var k = 0
      if(s%2!=0){
        for(var i=0;i!=2;i++)
          for(var j=0;j!=2;j++)
            if(i==0){
              point.points[k].x = x+(j+t+0.5)*width
              point.points[k].y = y
              k++
            }
            else{
              point.points[k].x = x + (j+0.5-t) * width
              point.points[k].y = y + width
              k++      
            }
      }
      else{
        for(var i=0;i!=2;i++)
          for(var j = 0;j!=2;j++)
            if(i==0){
              point.points[k].x = x
              point.points[k].y = y + (0.5 - t + j) * width
              k++
            }
            else{
              point.points[k].x = x+width
              point.points[k].y = y + (0.5 + t + j) * width
              k++
            }
        
      }
      DrawRect(point)
      brush.stroke()
      return get_point(maxy,point)
    }
    var t4 = function(s,x,y,t){
      var maxy = -1
      var point = new pointobj()
      point.bordercolor = BorderColor
      point.fillcolor = FillColor
      if(s==1){
        for(var i=0;i!=3;i++){
          point.points[i].x = x+width*i
          point.points[i].y = y+width
        }
        point.points[3].x = x+t*width
        point.points[3].y = y
      }
      else if(s==2){
        for (var i = 0; i != 3; i++){
          point.points[i].x = x
          point.points[i].y = y+width*i
        }
        point.points[3].x = x+width
        point.points[3].y = y+t*width
      }
      else if(s==3){
        for (var i = 0; i != 3; i++){
          point.points[i].x = x+width*i
          point.points[i].y = y
        }
        if(t==0){
          point.points[3].x = x+2*width
          point.points[3].y = y+width
        }
        else{
          point.points[3].x = x
          point.points[3].y = y+width
        }
      }
      else{
        if(t==0){
          point.points[3].x = x
          point.points[3].y = y+2*width
          for(var i=0;i!=3;i++){
          point.points[i].x = x+width
          point.points[i].y = y+width*i
          }
        }
        else{
          point.points[3].x = x
          point.points[3].y = y
          for(var i=0;i!=3;i++){
          point.points[i].x = x+width
          point.points[i].y = y+width*i
          }
        }
      }
      brush.stroke()
      DrawRect(point)
      return get_point(maxy,point)
    }

    var t5 = function(s,x,y){
      var maxy = -1
      var point = new pointobj()
      point.bordercolor = BorderColor
      point.fillcolor = FillColor
      if(s==1){
        point.points[0].x = x+width
        point.points[0].y = y
        for(var i=0;i!=3;i++){
          point.points[i+1].x = x+width*i
          point.points[i+1].y = y+width
        }
      }
      else if(s==2){
        for(var i=0;i!=3;i++){
        point.points[i].x = x
        point.points[i].y = y+width*i
        }
        point.points[3].x = x+width
        point.points[3].y = y+width
      }
      else if(s==3){
        for(var i=0;i!=3;i++){
        point.points[i].x = x+i*width
        point.points[i].y = y
        }
        point.points[3].x = x+width
        point.points[3].y = y+width
      }
      else{
        point.points[3].x = x
        point.points[3].y = y+width
        for(var i=0;i!=3;i++){
        point.points[i].x = x+width
        point.points[i].y = y+i*width
        }
      }
      brush.stroke()
      DrawRect(point)
      return get_point(maxy,point)
    }

    function get_point(maxy,point){
      var c = false
      for (var i = 0; i != 4; i++) {
        if (GameMap[point.points[i].y / width+1][point.points[i].x / width].canplace == false) {
          c = true
          break
        }
      }
      return {
        can: c,
        Point: point
      }
    }
    function CanPlace(p1,p2){
      if(p1.y+width!=p2.y) return true
      return false
    }


    function Draw(first,second){
      var obj=null
      if(first == 1)
        obj = t4(state,x1,y1,second)
      else if(first == 0)
        obj = t1(state,x1,y1)
      else if(first ==2)
        obj = t2(x1,y1)
      else if(first == 3)
        obj = t3(state,x1,y1,second)
      else 
        obj = t5(state,x1,y1)
      return obj
    }
    var that = this
    function drop()
    {  
      if(Continue==false)
      return
      framenum++
      if(framenum%that.data.mod== 0)
      {
        counter++
        y1 = width * counter
        if(y1+width*maxrow==maxv*width) counter=-1


        var obj =Draw(First,Second)
        if(obj.can==true){
          setParam()
          counter = -1
          x1 = 3*width
          Save.push(obj.Point)
          var o = obj.Point
          for(var i=0;i!=4;i++){
            GameMap[o.points[i].y/width][o.points[i].x/width].canplace = false
          }
          /*
          for(var i=0;i!=maxh;i++)
          if(GameMap[0][i].canplace==false){
            wx.showModal({
              title: '游戏结束',
              content: '总得分：'+that.data.Score,
              confirmText:"继续",
              success(res) {
              if (res.cancel) {
                  console.log('用户点击取消')
                  //Continue=false
                }
              }
            })
          }
          */

          judge()
          if(Save_destroy.length!=0){
            Clear()
            for (var i = 0; i != maxv; i++)
              for (var j = 0; j != maxh; j++)
                GameMap[i][j].canplace = true
            for (var i = 0; i != Save.length; i++)
              for (var j = 0; j != 4; j++)
                if (Save[i].points[j].y != -1) {
                  GameMap[Save[i].points[j].y / width][Save[i].points[j].x / width].canplace = false
                }
            that.setData({Score:that.data.Score+add})
            add = 0
            Save_destroy=[]
          }
        }
        brush.setFillStyle("red")
        //brush.fill()
        brush.draw()
        draw()
        

      }
     // requestAnimationFrame(drop)
    }
    function DrawRect(obj){
      for (var i = 0; i != maxv; i++)
        for (var j = 0; j != maxh; j++)
          if (GameMap[i][j].canplace == true) {
            brush.setStrokeStyle('#ccc')
            brush.strokeRect(GameMap[i][j].x, GameMap[i][j].y - width, width, width)
            brush.setFillStyle('#ccc')
            brush.fillRect(GameMap[i][j].x + Border, GameMap[i][j].y - width + Border, width - 2 * Border, width - 2 * Border)
          }
      for (var j = 0; j != 4; j++)
        if (obj.points[j].y != -1) {
          brush.setStrokeStyle(obj.bordercolor)
          brush.strokeRect(obj.points[j].x,obj.points[j].y, width, width)
          brush.setFillStyle(obj.fillcolor)
          brush.fillRect(obj.points[j].x + Border, obj.points[j].y + Border, width - 2 * Border, width - 2 * Border)
        }
    }
    function draw(){
      for(var i=0;i!=Save.length;i++)
      DrawRect(Save[i])
    }
    var that = this
    wx.getSystemInfo({
      success(res){
        windowheight = res.windowHeight
        windowwidth = res.windowWidth
        maxh = parseInt(windowwidth/width)
        maxv = parseInt((windowheight-40)/width)
        console.log(maxh,maxv)
        that.setData({ height: (maxh+7)*width, width:maxh*width-2})
        for(var i=0;i!=maxv+1;i++){
          var l = []
          var t = true
          if(i==maxv) t = false
         for(var j = 0;j!=maxh;j++)
         l.push({
           x:width*j,
           y:width*(i+1),
           canplace:t
         })
         GameMap.push(l)
        }
        setInterval(function e(){
          drop()

        },20)
        //drop() 
      }

      
    })
  }
})
