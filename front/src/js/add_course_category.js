function CourseCategory() {

}
//添加新闻分类
CourseCategory.prototype.ListenAddBtnEvent = function(){
    var addBtn = $('#addBtn');
    addBtn.click(function (event) {
        event.preventDefault();
        xfzalert.alertOneInput({
            'title':'请输入课程分类',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/add_course_category/',
                    'data':{
                        'name':inputValue,
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
CourseCategory.prototype.ListenEditBtnEvent = function(){
    var editBtn = $('.edit-btn');
    editBtn.click(function (event) {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        event.preventDefault();
        xfzalert.alertOneInput({
            'title':'修改分类名称',
            'placeholder':name,
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/edit_course_category/',
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
CourseCategory.prototype.ListenDelBtnEvent = function(){
    var delBtn = $('.del-btn');
    delBtn.click(function (event) {
        event.preventDefault();
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'title':'确认删除该分类？',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/del_course_category/',
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

CourseCategory.prototype.run = function(){
    var self = this;
    self.ListenAddBtnEvent();
    self.ListenEditBtnEvent();
    self.ListenDelBtnEvent();
};

$(function () {
    var category = new CourseCategory();
    category.run();
});