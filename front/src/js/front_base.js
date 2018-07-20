// 显示用户更多信息代码

function FrontBase() {

}
FrontBase.prototype.run = function () {
    var self = this;
    self.ListenUserBox();
};

FrontBase.prototype.ListenUserBox = function () {
  var authBox= $('.auth-box');
  var userMoreBox = $('.user-more-box');
  authBox.hover(function () {
      userMoreBox.show();
  },function () {
      userMoreBox.hide();
  })
};

$(function () {
   var frontBase = new FrontBase();
   frontBase.run();
});

// # 用户登录注册的js代码



function Auth() {
    this.scrollWrapper = $('.scroll-wrapper');
    this.maskWrapper = $('.mask-wrapper');
    this.smsCapthaBtn = $('#sms-captcha');
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

// # 登录
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
       if(!telephone || !password){
           window.messageBox.showInfo('请输入完整的账号信息！')
       }
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
                       window.messageBox.showError(messageObject)
                   }else {
                       // {'username':['xxxxxxxxxxxxxxx','xxx'],'telephone':['xxxxxxx','xxxxxx']}
                       console.log(messageObject);
                       for(var key in messageObject){
                           var messages = messageObject[key];
                           var message = messages[0];
                           window.messageBox.showError(message)
                       }
                   }
               }
           },
           'fail':function (error) {
               window.messageBox.showError(error)
           }
       });

    });
};
// 注册
Auth.prototype.ListensignupEvent = function(){
    var signupGroup = $('.signup-group');
    var telephoneInput = signupGroup.find("input[name='telephone']");
    var smscaptchaInput = signupGroup.find("input[name='sms_captcha']");
    var imgcaptchaInput = signupGroup.find("input[name='img_captcha']");
    var usernameInput = signupGroup.find("input[name='username']");
    var password1Input = signupGroup.find("input[name='password1']");
    var password2Input = signupGroup.find("input[name='password2']");
    var signupBtn = signupGroup.find('.submit-btn');

    signupBtn.click(function (event) {
        event.preventDefault();
        var telephone = telephoneInput.val();
        var sms_captcha = smscaptchaInput.val();
        var img_captcha = imgcaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var username = usernameInput.val();

        if(!telephone){
            window.messageBox.showError('请输入手机号');
            return;
        }
         if(!username){
            window.messageBox.showError('请输入用户名');
            return;
        }
         if(!password1){
            window.messageBox.showError('请输入密码');
            return;
        }
         if(!password2){
            window.messageBox.showError('请再次确认密码');
            return;
        }
         if(!sms_captcha){
            window.messageBox.showError('请输入验证码');
            return;
        }
        if (!img_captcha) {
            window.messageBox.showError('请输入验证码');
            return;
        }
        xfzajax.post({
            'url':'/account/signup/',
            'data':{
                'telephone':telephone,
                'username':username,
                'password1':password1,
                'password2':password2,
                'img_captcha':img_captcha,
                'sms_captcha':sms_captcha
            },
            'success':function (result) {
                if (result['code'] == 200){
                    window.location.reload()
                }else {
                    // 根据需求，forms中已经将get_errors的返回值处理为字典格式
                    var messageObject = result['message'];
                    if (typeof messageObject == 'string' || messageObject.constructor == String) {
                        window.messageBox.showError(messageObject)
                    } else {
                        // {'username':['xxxxxxxxxxxxxxx','xxx'],'telephone':['xxxxxxx','xxxxxx']}
                        console.log(messageObject);
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.showError(message)
                        }
                    }
                }
            },
            'fail':function (error) {
                window.messageBox.showError(error)
            }
        })
    })
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
// 图形验证码点击变换事件
Auth.prototype.ListenimgCaptcha = function(){
    var imgCaptcha = $('#captcha-img');
    imgCaptcha.click(function () {
       imgCaptcha.attr('src','/account/img_captcha/'+'?=random'+Math.random())
    });
};
//  验证码成功发送事件
Auth.prototype.ListensmsSuccessSend = function(){
    var self = this;
    window.messageBox.showSuccess('发送成功，请注意查收');
    self.smsCapthaBtn.addClass('disabled');
    var count = 10;
    self.smsCapthaBtn.unbind('click');
    var timer = setInterval(function () {
        self.smsCapthaBtn.text(count + 's');
        count -= 1;
        if (count <= 0) {
            self.smsCapthaBtn.removeClass('disabled');
            clearInterval(timer);
            self.smsCapthaBtn.text('发送验证码');
            self.ListensmsCaptchaEvent();
        }
    }, 1000)
};
// 短信验证码发送事件
Auth.prototype.ListensmsCaptchaEvent = function(){
    var self = this;
    var signupGroup = $('.signup-group');
    var telephoneInput = signupGroup.find("input[name='telephone']");

    self.smsCapthaBtn.click(function (event) {
        event.preventDefault();
        var telephone = telephoneInput.val();
        //获取时间戳
        var timestamp = (new Date).getTime();
        // 生成一个sign ,用于验证！
        var sign = md5(telephone + timestamp + 'dagfdv!@$%$#^ghgdafdvsafa$@$#');
        console.log(timestamp);
        if (!(/^1[35789]\d{9}$/.test(telephone))) {
            window.messageBox.showError('请输入正确的手机号！');
            return;
        }
        xfzajax.post({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone,
                'timestamp':timestamp,
                'sign':sign
            },
            'success': function (result) {
                if (result['code'] == 200) {
                    self.ListensmsSuccessSend();
                } else {
                    window.messageBox.showError(result['message']);
                }
            },
            'fail': function (error) {
                window.messageBox.showError(error)
            }
        })
    })
};
// 入口函数
Auth.prototype.run = function () {
    this.ListenBtnClick();
    this.Switch();
    this.ListenSigninBtnClick();
    this.ListenimgCaptcha();
    this.ListensmsCaptchaEvent(); //短信验证码
    this.ListensignupEvent();// 用户注册
};

$(function () {
    var auth = new Auth();
    auth.run();
});
$(function () {
       // art-template模板过滤器
    template.defaults.imports.timesince = function (valueDate) {
        var date = new Date(valueDate);
        var dates = date.getTime();
        var now = (new Date()).getTime();
        var timestamp = (now-dates)/1000;
        if(timestamp<60){
            return '刚刚';
        }
        else if(timestamp>60 && timestamp<60*60){
              minutes = parseInt(timestamp/60);
            return  minutes+'分钟前';
        }
        else if (timestamp>60*60 && timestamp<60*60*24) {
            hours = parseInt(timestamp/(60*60));
            return hours+'小时前';
        }

        else if(timestamp>60*60*24 && timestamp <60*60*24*30)
        {
            days = parseInt(timestamp/(60*60*24));
            return days+'天前';
        }else {
            var year = date.getFullYear();
            var month = date.getMonth();
            var day = date.getDay();
            var hour = date.getHours();
            var min = date.getMinutes();
            return year+'/'+month+'/'+day+'/'+hour+'/'+min;
        }

    }
});
// # 图形验证码刷新
// $(function () {
//     $('#captcha-img').click(function (event) {
//         var self = $(this);
//         var src = self.attr('src');
//         var newsrc = zlparam.setParam(src,'xx',Math.random());
//         self.attr('src',newsrc);
//     })
// });
