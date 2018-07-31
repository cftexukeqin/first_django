function CMSNewsList() {

}
CMSNewsList.prototype.initDatetimepicker = function(){
    var startpicker = $('#startpicker');
    var endpicker = $('#endpicker');
    var todaydate = new Date();
    var today = todaydate.getFullYear()+'/'+(todaydate.getMonth()+1)+'/'+todaydate.getDate();
    var options = {
        "format": 'yyyy/mm/dd',  //显示格式可为yyyymm/yyyy-mm-dd/yyyy.mm.dd
        // weekStart: 1,  	//0-周日,6-周六 。默认为0
        "language":'zh-CN',
        "showButtonPanel":true,
        "startDate":'2018/6/1',
        "endDate":today,
        "autoclose": true,
	    "todayBtn":'linked', 	//true时"今天"按钮仅仅将视图转到当天的日期。如果是'linked'，当天日期将会被选中。
        "clearBtn":true,
	    "todayHighlight":true,	//默认值: false,如果为true, 高亮当前日期。
    };
    startpicker.datepicker(options);
    endpicker.datepicker(options);
};
CMSNewsList.prototype.listenDeleteEvent = function(){
    var deleteBtn = $('.del-btn');
    var tr = deleteBtn.parent().parent();
    var newsId = tr.attr('data-pk');
    deleteBtn.click(function () {
        xfzalert.alertConfirm({
        'title':'确认删除这篇新闻?',
        'confirmCallback':function () {
            xfzajax.post({
                'url':'/cms/del_news/',
                'data':{
                    'pk':newsId
                },
                'success':function (result) {
                    if(result['code'] === 200){
                        window.messageBox.showSuccess('删除成功！');
                        window.location.reload()
                    }
                }
            })
        }
    })
    })
};
CMSNewsList.prototype.run = function () {
    this.initDatetimepicker();
    this.listenDeleteEvent();
};
$(function () {
   var cmsnewslist = new CMSNewsList();
   cmsnewslist.run();
});