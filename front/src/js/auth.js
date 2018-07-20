
// #点击登录按钮，弹出模态对话框
// $(function () {
//     $("#btn").click(function () {
//         $(".mask-wrapper").show();
//     });
//
//     $(".close-btn").click(function () {
//         $(".mask-wrapper").hide();
//     });
// });


function Auth() {
    this.scrollWrapper = $('.scroll-wrapper');
    this.maskWrapper = $('.mask-wrapper');
}


Auth.prototype.ShowEvent = function () {
    var self = this;
    self.maskWrapper.show();
};

Auth.prototype.HideEvent = function () {
    var self = this;
    self.maskWrapper.hide();
};

Auth.prototype.ListenBtnClick = function () {
    var self = this;
    var signinBtn = $('.signin-btn');
    var signupBtn = $('.signup-btn');
    var closeBtn = $('.close-btn');
    signinBtn.click(function () {
        self.ShowEvent();
        self.scrollWrapper.css({'left':0})
    });
    signupBtn.click(function () {
        self.ShowEvent();
        self.scrollWrapper.css({'left':'-400px'})
    });
    closeBtn.click(function () {
       self.HideEvent()
    });
};

Auth.prototype.ListenSigninBtnClick = function(){
    var self = this;
    var signinGroup = $('.signin-group');
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");
    var submitBtn = signinGroup.find('.submit-btn');

    submitBtn.click(function () {
       telephone = telephoneInput.val();
       password = passwordInput.val();
       remember =rememberInput.prop('checked');

       xfzajax.post({
           'url':'/account/login/',
           'data':{
               'telephone':telephone,
               'password':password,
               'remember':remember?1:0
           },
           'success':function (result) {
               if(result['code'] == 200){
                   self.HideEvent();
                   window.location.reload()
               }else {
                   // 根据需求，forms中已经将get_errors的返回值处理为字典格式
                   var messageObject = result['message'];
                   if(typeof messageObject == 'string'|| messageObject.constructor == String ){
                       window.messageBox.show(messageObject);
                   }else {
                       // {'username':['xxxxxxxxxxxxxxx','xxx'],'telephone':['xxxxxxx','xxxxxx']}
                       for(var key in messageObject){
                           var messages = messageObject[key];
                           var message = messages[0];
                           window.messageBox.show(message)
                       }
                   }
               }
           },
           'fail':function (error) {
               window.messageBox.show(error)
           }
       });

    });
};

Auth.prototype.Switch = function(){
    var self = this;
    var switchBtn = $('.switch');
    switchBtn.click(function () {
        var currentLeft = self.scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            self.scrollWrapper.animate({"left": '0'});
        } else {
            self.scrollWrapper.animate({"left": "-400px"});
        }
    });
};
// 入口函数
Auth.prototype.run = function () {
    this.ListenBtnClick();
    this.Switch();
    this.ListenSigninBtnClick();
};

$(function () {
    var auth = new Auth();
    auth.run();
});