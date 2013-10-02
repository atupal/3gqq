/*
 * author: atupal
 * file: kvdbmanage.js
 * date: 2/10/2013
 * */

$(function(){
    $(".value").each(function(index, ele){
      this.innerHTML = this.innerHTML.replace(/\s/g, '');
      this.className = "value_s";
      this.style.whiteSpace="pre-wrap";
      //ele.innerHTML = JSON.stringify( JSON.parse(ele.innerHTML), null, 4 );
      //ele.style.whiteSpace="pre-wrap";

      ele.onclick = function(){
      if (this.className == "value") {
      this.innerHTML = this.innerHTML.replace(/\s/g, '');
      this.className = "value_s";
      } else {
      this.innerHTML = JSON.stringify( JSON.parse(this.innerHTML), null, 4 );
      this.className = "value";
      }
      }

      });


    $("#format")[0].onclick = function(){
      var a = $("#format")[0]
        if (a.innerHTML == "unformat") {
          $(".value").each(function(index, ele){
              ele.innerHTML = ele.innerHTML.replace(/\s/g, '');
              ele.className = "value_s";
              });
          a.innerHTML = "format";
        } 
        else {
          $(".value_s").each(function(index, ele){
              ele.innerHTML = JSON.stringify( JSON.parse(ele.innerHTML), null, 4 );
              ele.className = "value";
              });
          a.innerHTML = "unformat";
        }
    };

});
