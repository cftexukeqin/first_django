function OrderList() {

}
OrderList.prototype.listenDelBtnEvent = function(){
    var delBtn = $('.del-btn');
    delBtn.click(function () {
        var currrentBtn = $(this);
        var orderId = currrentBtn.attr('data-order-id');
        xfzalert.alertConfirm({
            'title':'确定删除此订单？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/course/del_course/',
                    'data':{
                        'order_id':orderId
                    },
                    'success':function (reslut) {
                        if (reslut['code'] === 200){
                            window.messageBox.showSuccess('删除成功！');
                            window.location.reload()
                        } else {
                            window.messageBox.showError(reslut['message'])
                        }

                    }
                })
            }
        })
    })
};

OrderList.prototype.run = function () {
    this.listenDelBtnEvent();
};
$(function () {
   var order = new OrderList();
   order.run();
});