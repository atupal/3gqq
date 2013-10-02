/*
 * author: atupal
 * file: signup.js
 * date: 2/10/2013
 * */

$(function(){
  $("form").submit(function(){
    if (!$("[name=email]")[0].value || $("[name=email]")[0].value.length < 6) {
      alert("请填写邮箱！");
      return false;
    }

    if (!$("[name=qq]")[0].value || $("[name=qq]")[0].value.length < 6) {
      alert("请填写正确的QQ号码");
      return false;
    }

    if (!$("[name=qq]")[0].value || $("[name=qq]")[0].value.length < 6) {
      alert("请填写正确的QQ号码");
      return false;
    }

    if ($("[name=password]")[0].value != $("[name=password-re]")[0].value) {
      alert("密码不一致");
      return false;
    }

    if (!$("[name=password]")[0].value || $("[name=password]")[0].value.length < 6) {
      alert("密码不能少于6位数");
      return false;
    }

    $.ajax({
      type: 'POST',
      url: '/signup',
      data: $("form").serialize()
    })
    .success(function(data){
      var ret = {code: "-1", msg: "error"};
      try{
        ret = JSON.parse(data);
      } catch(e){
      };
      alert(ret.msg);
    }).fail(function(a, b, data){
    });

    return false;
  });
});
