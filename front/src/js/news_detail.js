function NewsList() {
    var self = this;
    self.maskWrapper = $('.mask-wrapper');
}
NewsList.prototype.ListenSubmitBtnClick = function(){
    var self = this;
    var submitBtn = $('.commit-btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-id');
        xfzajax.post({
            'url':'/news/pub_comment/',
            'data':{
                'content':content,
                'news_id':news_id,
            },
            'success':function (result) {
                if(result['code'] === 200){
                    var comment = result['data'];
                    var tpl = template('comment-item',{'comment':comment});
                    var commentList = $('.comment-list');
                    commentList.prepend(tpl);
                    textarea.val("");
                    window.messageBox.showSuccess('评论成功！')
                }else {
                    self.maskWrapper.show();
                }
            },
            'fail':function (err) {
                window.messageBox.showError(err);
            }
        })
    })
};
NewsList.prototype.run = function () {
    this.ListenSubmitBtnClick();
};
$(function () {
   var newslist  = new NewsList();
   newslist.run();
});