// pages/index/index.js
var startx=0;
var starty=0;
var movex=0;
var movey=0;
var X=0;
var Y=0;
var width=0;
var height=0;
var snakeheader={
  x:0,
  y:0,
  width:10,
  height:10
}
var snakebody=[];
var foods=[]
var remove = true

var direction="Right";
var snakedirect = "Right";
var framenum=0
Page({
  data: {
    src: 'https://m10.music.126.net/20190215161320/3a49f58fc929bc003b9ed6ed225f46ab/ymusic/d49a/7916/6564/74943f700c2cdbee9bdc447644471e8f.mp3'

  },
  canvasStart:function(e){
    startx=e.touches[0].x
    starty=e.touches[0].y
  },
  canvasMove:function(e){
    movex=e.touches[0].x
    movey=e.touches[0].y
    X = movex-startx
    Y = movey - starty
    if(Math.abs(X)>Math.abs(Y))
    {
      if(X>0) direction="Right"
      else direction="Left"
    }
    else{
      if(Y>0) direction="Down"
      else direction="Up"
    }
  },
  canvasEnd:function(){
    if(direction=="Right"&&snakedirect!="Left")
      snakedirect = direction
    else if(direction=="Left"&&snakedirect!="Right")
      snakedirect = direction
    else if(direction=="Down"&&snakedirect!="Up")
      snakedirect = direction
    else if(direction=="Up"&&snakedirect!="Down")
      snakedirect = direction
  },
  onReady:function(){
    this.audio = wx.createInnerAudioContext()
    this.audio.src = this.data.src
    this.audio.autoplay=true
    this.audio.loop = true
    var brush = wx.createCanvasContext('snakecanvas');
    //碰撞判断函数
    function collide(header, food) {
      if (header.y <= food.y + food.height && header.y + header.height >= food.y && header.x <= food.x + food.width && food.x <= header.x + header.width)
        {
          return true
        }
    }
    //动画主体
    function animate(){
      framenum++;
      if(framenum%20==0){
        snakebody.push({
          x: snakeheader.x,
          y: snakeheader.y,
          width: snakeheader.width,
          height: snakeheader.height,
          color: "#00ff00"
        })


        switch (snakedirect) {
          case "Left":
            snakeheader.x -= snakeheader.width
            break;
          case "Right":
            snakeheader.x += snakeheader.width
            break;
          case "Down":
            snakeheader.y += snakeheader.height
            break;
          case "Up":
            snakeheader.y -= snakeheader.height
            break;
        }
        remove = true
        for(var i=0;i<foods.length;i++)
        {
          if(collide(snakeheader,foods[i]))
          {
            remove = false
            foods[i].x = rand(0,width)
            foods[i].y = rand(0,height)
            break
          }
        }
        if (snakebody.length > 4 && remove) {
          snakebody.shift()
          remove = true
        }
        if(snakeheader.y-snakeheader.height>=height) snakeheader.y=0
        if(snakeheader.x - snakeheader.width>=width) snakeheader.x =0
        if(snakeheader.y<0) snakeheader.y = height-snakeheader.height
        if(snakeheader.x<0) snakeheader.x = width-snakeheader.width
      }
      brush.drawImage('image/'+snakedirect+".jpg",snakeheader.x,snakeheader.y,snakeheader.width,snakeheader.width)
      for(var i=0;i<snakebody.length;i++){
        brush.drawImage('image/food.jpg', snakebody[i].x, snakebody[i].y, snakebody[i].width, snakebody[i].height)
      }
      for(var i=0;i<foods.length;i++){
        brush.setFillStyle(foods[i].color)
        brush.fillRect(foods[i].x,foods[i].y,foods[i].width,foods[i].height)
      }
      brush.draw()
      
    }
    //随机数
    function rand(min,max){
      return parseInt(Math.random()*(max-min))
    }
    //食物对象
    function Food(){
      this.x = rand(0,width)
      this.y = rand(0,height)
      this.width = 8
      this.height = 8
      this.color = "rgb("+rand(0,255)+","+rand(0,255)+","+rand(0,255)+")"
    }
    //获取屏幕高宽
    wx.getSystemInfo({
      success:function(res){
        width=res.windowWidth;
        height=res.windowHeight;
        for(var i=0;i<20;i++){
          var food = new Food();
          foods.push(food)
        }
        //animate();
        var interval = setInterval(function c() {
         animate()
        },20)
      }
    })
  }
})