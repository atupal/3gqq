/*
 * author: atupal
 * file: feedback.js
 * data: 2/10/2013
 * */

$(function(){
  $('form').submit(function(){
    if(!$('[name=nickname]')[0].value) {
      $( ".btn-warn").text("请填写昵称！").show().fadeOut(1000);
      return false;
    }
    if(!$('[name=contact]')[0].value) {
      $(".btn-warn").text("请填写联系方式称！").show().fadeOut(1000);
      return false;
    }
    if(!$('[name=comment]')[0].value) {
      $(".btn-warn").text("请填写评论!！").show().fadeOut(1000);
      return false;
    }
  });
});
