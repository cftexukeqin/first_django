function News() {
    var self = this;
}

//实例化百度富文本编辑器
News.prototype.UeditorEvent = function(){
    var ue = UE.getEditor('container',{
            'initialFrameHeight': 400,
            'serverUrl': '/ueditor/upload/'
        });
    window.ue = ue
};
News.prototype.AddNewsEvent = function(){
    var submitBtn = $('#submit-Btn');
    var titleInput = $("input[name='title']");
    var categorySelect = $("select[name='category']");
    var descInput = $("input[name='desc']");
    var thumbnailInput = $("input[name='thumbnail']");
    var pk = submitBtn.attr('data-news-id');
    console.log(pk);
    submitBtn.click(function (event) {
        event.preventDefault();
        var title = titleInput.val();
        var category = categorySelect.val();
        var desc = descInput.val();
        var thumbnail = thumbnailInput.val();
        var content = ue.getContent();
        var url = '';
        if(pk){
            url = '/cms/edit_news/';
        }else {
            url = '/cms/add_news/';
        }
        if(!title||!category||!desc||!thumbnail||!content){
            window.messageBox.showError('请输入新闻完整信息！');
            return;
        }
        xfzajax.post({
            'url':url,
            'data':{
                'title':title,
                'category':category,
                'desc':desc,
                'thumbnail':thumbnail,
                'content':content,
                'pk':pk
            },
            'success':function (result) {
                if(result['code'] === 200){
                    if(pk){
                        xfzalert.alertSuccessToast('新闻编辑成功！');
                    }else {
                        xfzalert.alertSuccessToast('新闻发布成功！');
                    }
                    window.location = '/cms/news_lists/';
                }
            },
            'fail':function (error) {
                xfzalert.alertInfoToast(error)
            }
        })
    })
};

// 上传到本地服务器设置
News.prototype.listenUploadFileEvent = function(){
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formdata = new FormData();
        formdata.append('file', file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data': formdata,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var imgUrl = result['data']['url'];
                    var urlInput = $("input[name='thumbnail']");
                    urlInput.val(imgUrl);
                }
            }
        })
    })
};
// 上传到七牛云
News.prototype.listenQiniuUploadEvent = function(){
    var self = this;
        var uploadBtn = $('#thumbnail-btn');
        uploadBtn.change(function () {
            var file = this.files[0];
            xfzajax.get({
                'url':'/cms/qntoken/',
                'success':function (result) {
                    if(result['code'] === 200){
                        var token = result['data']['token'];
                        var key = (new Date()).getTime()+'.'+file.name.split('.')[1];
                        var putExtra = {
                            'fname':key,
                            'params':{},
                            'mimeType':['image/png','image/jpeg','image/gif','video/mp4']
                        };
                        var config = {
                            'userCdnDomain':true,
                            'retryCount':6,
                            'region':qiniu.region.z1,
                        };
                        var observable = qiniu.upload(file,key,token,putExtra,config);
                        observable.subscribe({
                            'next':self.QiniuUploadNext,
                            'error':self.QiniuUploadError,
                            'complete':self.QiniuUploadComplete
                        })
                    }
                }
            })
        })
};
// 文件上传next，会有上传的进度信息
News.prototype.QiniuUploadNext = function(res){
    var total = res.total;
    var percent = total.percent;
    var progessGroup = $('#progess-group');
    var progessbar = $('.progress-bar');
    progessbar.css({'width':0});
    progessGroup.show();
    progessbar.css({'width':percent+'%'});
    progessbar.text(percent.toFixed()+'%');
};
News.prototype.QiniuUploadError = function(err){
    err='上传文件类型错误，请选择图片文件！';
    xfzalert.alertErrorToast(err);
    // window.messageBox.showError(err);
};
News.prototype.QiniuUploadComplete = function(res){
    var filename = res['key'];
    var domain = 'http://pbci7ji9t.bkt.clouddn.com/';
    var progessGroup = $('#progess-group');
    var fileInput = $("input[name='thumbnail']");
    fileInput.val(domain+filename);
    progessGroup.hide();

};
News.prototype.run = function () {
    var self = this;
    // self.listenUploadFileEvent();
    self.listenQiniuUploadEvent();
    self.UeditorEvent();
    self.AddNewsEvent();
};

$(function () {
   var news = new News();
   news.run();
});