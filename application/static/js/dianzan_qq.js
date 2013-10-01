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

    if ($("#verify_div").hasClass("hidden")) {
      $.ajax({
        type: 'POST',
        url: 'dianzan',
        data: $('form').serialize()
      })
      .success(function(data){
        var ret = data.trim();
        if (ret == "success") {
          alert("赞成功!");
        } else if (ret.indexOf('<html>') != -1) {
          var dstFrame = document.getElementById('iframe_verify');
          var dstDoc = dstFrame.contentDocument || dstFrame.contentWindow.document;
          dstDoc.write(ret);
          dstDoc.close();
          $(".verify_img")[0].src=dstDoc.getElementsByTagName("img")[0].src;
          $("#verify_div").removeClass("hidden");
        }
      })
      .fail(function(a, b, data){
        alert(data);
      });
    } else {
      var node = $("[name=verify]")[0];
      if ((! node.value) || node.value.length != 4) {
        $("[for=verify]").text("请输入4位验证码").show().fadeOut(1000);
        return false;
      }
      var dstFrame = document.getElementById('iframe_verify');
      var dstDoc = dstFrame.contentDocument || dstFrame.contentWindow.document;
      var dst = $(dstDoc.getElementsByTagName("form")[0]);
      dst.children("[name=verify]")[0].value = node.value;
      $.ajax({
        type: 'POST',
        url: 'dianzan_verify',
        data: dst.serialize()
      })
      .success(function(data){
        var ret = data.trim();
        if (ret == "success") {
          $("#verify_div").addClass("hidden");
          alert("赞成功!");
        } else {
          $("[for=verify]").text("验证码不正确").show().fadeOut(1000);
          $("#verify_div").addClass("hidden");
          $("form").submit();
        }
      })
      .fail(function(a, b, data){
        alert(data);
      });
    }

    return false;
  });

  $(".verify_img").click(function(){
    this.src = this.src;
  });
});
