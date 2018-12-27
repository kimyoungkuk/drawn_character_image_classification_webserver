
  var pos = {
      drawable: false,
      x: -1,
      y: -1
  };
  var canvas, ctx;

  window.onload = function(){
      canvas = document.getElementById("canvas");
      ctx = canvas.getContext("2d");
      ctx.fillStyle = 'white'; // 채우기 색 지정
      ctx.globalAlpha = "1.0"; // 채우기 투명도 설정
      ctx.fillRect(0,0,500,500);
      fromDataURL(ctx);
      // var image = new Image();
      // image.src = canvas.toDataURL();
      //
      // image.onload = function(){
      //   ctx.drawImage(image,0,0);
      // }

      canvas.addEventListener("mousedown", listener);
      canvas.addEventListener("mousemove", listener);
      canvas.addEventListener("mouseup", listener);
      canvas.addEventListener("mouseout", listener);
      canvas.addEventListener("touchstart", listener);
      canvas.addEventListener("touchmove", listener);
      canvas.addEventListener("touchcancel", listener);
      canvas.addEventListener("touchend", listener);

  }

  function listener(event){

      switch(event.type){
          case "mousedown":
              initDraw(event);
              break;
          case "touchstart":
              initDraw(event);
              break;

          case "mousemove":
              if(pos.drawable)
                  draw(event);
              break;
          case "touchmove":
              if(pos.drawable)
                  draw(event);
              break;

          case "mouseout":
          case "touchcancel":

          case "mouseup":
              finishDraw();
              break;
          case "touchend":
              finishDraw();
              break;
      }
  }

  function initDraw(event){
      ctx.beginPath();
      pos.drawable = true;
      var coors = getPosition(event);
      pos.X = coors.X;
      pos.Y = coors.Y;
      ctx.moveTo(pos.X, pos.Y);

  }

  function draw(event){
      var coors = getPosition(event);
      ctx.lineTo(coors.X, coors.Y);
      pos.X = coors.X;
      pos.Y = coors.Y;
      ctx.stroke();
  }

  function finishDraw(){
      pos.drawable = false;
      pos.X = -1;
      pos.Y = -1;
  }

  function getPosition(event){
      var bound = canvas.getBoundingClientRect();
      var x = (event.x - bound.left) * (canvas.width / bound.width);
      var y = (event.y - bound.top) * (canvas.height / bound.height);
      return {X: x, Y: y};
  }
