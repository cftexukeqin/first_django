//jQuery 是一个高效、精简并且功能丰富的 JavaScript 工具库。它提供的 API 易于使用且兼容众多浏览器，
// 这让诸如 HTML 文档遍历和操作、事件处理、动画和 Ajax 操作更加简单。
// Jquery 面向对象编程
// 定义类，或者说函数，通过this 添加属性
// Class.prototpye.func = function(){}的形式定义方法
// function Banner() {
//     console.log('构造函数');
//     this.person = 'rabbit';
// }
// Banner.prototype.greet = function (word) {
//     console.log('定义函数',word)
// };
// var banner = new Banner();
// console.log(banner.person);
// banner.greet('xukeqin');


//  定义一个Banner 类，用过this.attr 添加属性
function Banner() {
    this.bannerWidth = 840;
    this.bannerGroup = $('#banner-group');
    this.index = 1;
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.bannerUl = $('#banner-ul');
    this.ilList = this.bannerUl.children('li');
    this.bannerCount = this.ilList.length;
    this.pageControl = $('.page-control');


}
// 定义箭头显示与否的函数
Banner.prototype.toggleArrow = function(isShow){
  var self = this;
  if(isShow){
      self.rightArrow.toggle();
      self.leftArrow.toggle();
  }else {
      self.rightArrow.hide();
      self.leftArrow.hide();
  }
};

// banner初始化函数
Banner.prototype.initBanner = function(){
    var self = this;
    // 分别获取到第一张和最后一张
    var firstbanner = self.ilList.eq(0).clone();
    var lastbanner = self.ilList.eq(self.bannerCount-1).clone();
    self.bannerUl.append(firstbanner);
    self.bannerUl.prepend(lastbanner);

    self.bannerUl.css({'width':self.bannerWidth*(self.bannerCount+2),'left':-self.bannerWidth});

};

// 小圆点初始化函数
Banner.prototype.initPageControl = function(){
    var self = this;
  // 获取到标签
    var pageControl = $('.page-control');
    for(var i=0;i<self.bannerCount;i++)
    {
        var circle = $('<li></li>');
        pageControl.append(circle);
        if(i===0){
            circle.addClass('active');
        }
    }
    pageControl.css({'width':12*self.bannerCount+16+(self.bannerCount-1)*16})
};

// 轮播图函数封装
Banner.prototype.animate = function(){
    var self = this;
    self.bannerUl.animate({'left':-840*self.index},500);
    // 移动的时候，获取当前是哪个li标签，然后给他添加一个active 类，
    // pageControl.children('li') 获取所有子li标签
    var index = self.index;
    if(index===0){
        index = self.bannerCount - 1;
    }else if (index === self.bannerCount + 1){
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active');
};

// 要求绝对定位和相对定位
// 轮播图移动函数
//  循环轮播的思路：
// 1.在最前面添加最后一张，在最后面添加第一张。然后循环到克隆的那一张时，快速跳到按顺序的下一张
Banner.prototype.loop = function(){
    var self = this;
    // bannerUl.css({'left':-840});
    self.timer = setInterval(function () {
        if(self.index >= (self.bannerCount+1)){
            // 此时立马跳到第二个=轮播图
            self.bannerUl.css({'left':-self.bannerWidth});
            self.index = 2;
        }else {
            self.index++;
        }
        self.animate()
    },2000);
};
// 监听Hover时间，鼠标移动到轮播图和从轮播图离开的效果
Banner.prototype.listenBannerGroup = function(){
    var self = this;
    // console.log('listen 函数里面的this:',this);
    self.bannerGroup.hover(function () {
        // 第一个函数，鼠标移动到上面的操作
        // console.log('listen 函数里面的self:',self);
        clearInterval(self.timer);
        // console.log('listen 函数里面的this:',this);
        self.toggleArrow(true);
    },function () {
        // 第二个函数，鼠标离开后执行的操作
        self.loop();
        self.toggleArrow(false);
    })
};

// 监听鼠标点击箭头事件
Banner.prototype.listenArrowClick = function(){
    //
    var self = this;
    self.leftArrow.click(function () {
        if(self.index === 0){
            self.bannerUl.css({'left':-self.bannerWidth*self.bannerCount});
            self.index = self.bannerCount - 1;
        }else{
            self.index--;
        }
        self.animate()
    });
    self.rightArrow.click(function () {
        if(self.index === self.bannerCount +1){
            self.bannerUl.css({'left':-self.bannerWidth});
            self.index = 2
        }else {
            self.index++;
        }
        self.animate()

    })
};

// 监听小圆点点击事件
Banner.prototype.listenPageControl = function(){
    // 获取到pageControl，也就是小圆点
    var self = this;
    self.pageControl.children('li').each(function (index,obj) {
        $(obj).click(function () {
            self.index = index + 1;
            self.animate();
            // $(obj).pageControl.children('li').eq(self.index).siblings().removeClass('active');
        })
    })
};


function Index(){
    var self = this;
    self.page = 2;
    self.category_id = 0;
    self.loadBtn = $('#load-more-btn');
}
Index.prototype.ListenCategorySwitchEvent = function(){
    var self = this;
    var tabGroup = $('.list-tab');
    tabGroup.children().click(function () {
        // 通过$(this)获取当前选中的li标签
        var li = $(this);
        // console.log('li',li);
        var category_id = li.attr('data-category');
        var page = 1;
        // console.log('进入到点击事件',category_id);
        xfzajax.get({
            'url':'/news/list/',
            'data':{
                'p':page,
                'category_id':category_id,
            },
            'success':function (result) {
                if(result['code'] === 200){
                    var newses = result['data'];
                    var listGroup = $('.list-inner-group');
                    var html = template('newslist', {'newses': newses});
                    listGroup.empty();
                    listGroup.append(html);
                    self.page = 2;
                    li.addClass('active').siblings().removeClass('active');
                    self.category_id = category_id;
                    self.loadBtn.show();
                }
            }
        })
    })
};
// 显示更多按钮点击事件，将JSON数据显示成模板文件
Index.prototype.ListenLoadMoreBtnEvent = function(){
    var self = this;
    var loadBtn = $('#load-more-btn');
    //点击按钮获取数据，前端显示出来
    loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id':self.category_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];
                    if(newses.length>0){
                        var listGroup = $('.list-inner-group');
                        var html = template('newslist', {'newses': newses});
                        listGroup.append(html);
                        self.page += 1;
                    }else{
                        loadBtn.hide();
                    }
                }
            }
        })
    })
};
Index.prototype.run = function(){
    var self = this;
    self.ListenLoadMoreBtnEvent();
    self.ListenCategorySwitchEvent();
};
// 定义函数入口
Banner.prototype.run = function () {
    // console.log('run函数里面的this:',this);
    this.initBanner(); //  banner 数量
    this.initPageControl(); // 小圆点数量
    this.loop(); // 轮播图循环滚动
    this.listenBannerGroup(); // 轮播图
    this.listenArrowClick(); // 监听鼠标点击箭头事件
    this.listenPageControl(); // 监听小圆点事件
    // console.log(this.pageControl.children('li'));

};

// $(function () {
//     $('#nav li').click(function () {
//         $(this).siblings('li').removeClass('active');
//         $(this).addClass('active');
//     })
// });
$(function () {
    var banner = new Banner();
    var index = new Index();
    index.run();
    banner.run();
});