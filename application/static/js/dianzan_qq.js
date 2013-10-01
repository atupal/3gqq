/*
 * author: atupal
 * file: dianzan_qq.js
 * date: 1/10/2013
 * */

$(function(){
  $("form").submit( function(e) {
    if (! ($("[name=qq]")[0].value) ) {
      $("[for=qq]").text("请输入QQ号码！").show().fadeOut(1000);
      return false;
    }

    if (! ($("[name=pwd]")[0].value) ) {
      $("[for=password]").text("请输入QQ密码！").show().fadeOut(1000);
      return false;
    }

    $.ajax({
      type: 'POST',
      url: 'dianzan',
      data: $('form').serialize()
    })
    .success(function(data){
      alert(data);
    })
    .fail(function(a, b, data){
      alert(data);
    });

    return false;
  });
});
