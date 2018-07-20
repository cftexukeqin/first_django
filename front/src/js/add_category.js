function NewsCategory() {

}
//添加新闻分类
NewsCategory.prototype.ListenAddBtnEvent = function(){
    var addBtn = $('#addBtn');
    addBtn.click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'title':'请输入新闻分类',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/add_category/',
                    'data':{
                        'category':inputValue,
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else {
                            xtalert.alertErrorToast(result['message'])
                        }
                    }
                })
            }
        });
    })
};

// 编辑新闻分类
NewsCategory.prototype.ListenEditBtnEvent = function(){
    var editBtn = $('.edit-btn');
    editBtn.click(function (event) {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        console.log(tr);
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        event.preventDefault();
        xtalert.alertOneInput({
            'title':'修改分类名称',
            'placeholder':name,
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/edit_category/',
                    'data':{
                        'pk':pk,
                        'name':inputValue,
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            console.log(inputValue);
                            window.location.reload();
                        }
                    }
                })
            }
        })
    })
};
// 删除分类
NewsCategory.prototype.ListenDelBtnEvent = function(){
    var delBtn = $('.del-btn');
    delBtn.click(function (event) {
        event.preventDefault();
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xtalert.alertConfirm({
            'title':'确认删除该分类？',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/del_category/',
                    'data':{
                        'pk':pk
                    },
                    'success':function (result) {
                        window.location.reload();
                    }
                })
            }
        })
    })
};

NewsCategory.prototype.run = function(){
    var self = this;
    self.ListenAddBtnEvent();
    self.ListenEditBtnEvent();
    self.ListenDelBtnEvent();
};

$(function () {
    var category = new NewsCategory();
    category.run();
});