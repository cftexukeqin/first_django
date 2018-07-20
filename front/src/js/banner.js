function Banner() {

}
Banner.prototype.LoadData = function(){
    var self = this;
    xfzajax.get({
        'url':'/cms/banner_list/',
        'success':function (result) {
            if(result['code'] === 200){
                 var banners = result['data'];
                console.log(banners);
                for (i=0;i<banners.length;i++){
                    var banner = banners[i];
                    self.CreateBannerEvent(banner);
                }
            }
        }
    })
};

Banner.prototype.CreateBannerEvent = function(banner){
    var self = this;
    var tpl = template('banner-item',{'banner':banner});
    var bannerList = $('.banner-list-group');
    var bannerItem = null;
    if(banner){
        bannerList.append(tpl);
        bannerItem = bannerList.find('.banner-item:last');
    }else {
        bannerList.prepend(tpl);
        bannerItem = bannerList.find('.banner-item:first');
    }
    self.ListernImgClickEvent(bannerItem);
    self.RemoveBannerEvent(bannerItem);
    self.addBannerBtnClickEvent(bannerItem);
};

Banner.prototype.ListenAddBtnClickEvent = function(){
    var self = this;
    var addBtn = $('.add-btn');
    addBtn.click(function () {
        var bannerListGroup = $('.banner-list-group');
        var length = bannerListGroup.children().length;
        console.log(length);
        console.log('.................');
        if (length >= 6) {
            window.messageBox.showInfo('最多只能添加6张轮播图！');
            return;
        }
        self.CreateBannerEvent();
    });
};

Banner.prototype.ListernImgClickEvent = function(bannerItem){
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    image.click(function () {
        // var that = $(this);
        // var imageInput = that.siblings('.image-input');
        imageInput.click();
    });
    imageInput.change(function () {
        var file = this.files[0];
        var formdata = new FormData();
        formdata.append('file',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formdata,
            'processData':false,
            'contentType':false,
            'success':function (result) {
                if (result['code'] === 200){
                    var imgurl = result['data']['url'];
                    image.attr('src',imgurl);
                }
            }
        })
    })
};

Banner.prototype.addBannerBtnClickEvent = function(bannerItem){
    var prioritySpan = bannerItem.find("span[class='priority']");
    var priorityTag = bannerItem.find("input[name='priority']");
    var imageTag = bannerItem.find('.thumbnail');
    var link_toTag = bannerItem.find("input[name='link_to']");
    var saveBtn = bannerItem.find('.save-btn');
    var bannerId = bannerItem.attr('data-banner-id');
    var url = '';
    if (bannerId) {
        url = '/cms/editbanner/';
    } else {
        url = '/cms/addbanner/';
    }
    saveBtn.click(function () {
        var priority = priorityTag.val();
        var link_to = link_toTag.val();
        var image_url = imageTag.attr('src');
        xfzajax.post({
            'url': url,
            'data': {
                'priority': priority,
                'image_url': image_url,
                'link_to': link_to,
                'pk':bannerId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if(bannerId){
                        window.messageBox.showSuccess('修改成功！');
                    }else {
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('添加成功！');
                    }
                    prioritySpan.text('优先级：'+ priority);
                }else {
                    console.log(result['message'])
                }
            },
            'fail':function (err) {
                console.log(err)
            }
        })
    })
};

Banner.prototype.RemoveBannerEvent = function(bannerItem){
    var closeBtn = bannerItem.find('.close-btn');
    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId) {
            xtalert.alertConfirm({
                'msg': '确认删除此轮播图？',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                bannerItem.remove();
                                window.messageBox.showSuccess('删除成功！')
                            }
                        }
                    })
                }
            })
        }else {
            bannerItem.remove();
        }
    })
};

Banner.prototype.run = function () {
    this.ListenAddBtnClickEvent();
    this.LoadData();
};
$(function () {
    var banner = new Banner();
    banner.run();
});