function CourseAdd() {

}
CourseAdd.prototype.initUeditor = function(){
    var ue = UE.getEditor('editor',{
        'serverUrl':'/ueditor/upload/'
    });
    window.ue = ue;
};
CourseAdd.prototype.listenAddBtnEvent = function(){
    var addBtn = $('#submit-Btn');
    addBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var category_id = $("select[name='category']").val();
        var teacher_id = $("select[name='teacher']").val();
        var video_url = $("input[name='video_url']").val();
        var cover_url = $('#cover-input').val();
        var price = $('#price-input').val();
        var duration = $('#duration-input').val();
        var desc = ue.getContent();
        console.log(category_id);
        console.log('---------------------');
        console.log(teacher_id);
        xfzajax.post({
            'url':'/cms/add_course/',
            'data':{
                'title':title,
                'category_id':category_id,
                'teacher_id':teacher_id,
                'video_url':video_url,
                'cover_url':cover_url,
                'price':price,
                'duration':duration,
                'desc':desc
            },
            'success':function (result) {
                if (result['code'] === 200){
                    window.messageBox.showSuccess('课程发布成功！')
                }else {
                    window.messageBox.showError(result['message'])
                }
            },
            'fail':function (err) {
                console.log(err)
            }
        })
    })
};
CourseAdd.prototype.run = function () {
    this.initUeditor();
    this.listenAddBtnEvent();
};
$(function () {
   var course = new CourseAdd();
   course.run();
});