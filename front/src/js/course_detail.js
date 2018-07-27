function CourseDetail() {

}
CourseDetail.prototype.initPlayVideo = function(){
    var span = $('#info-span');
    var videourl = span.attr('data-video-url');
    var cover_url = span.attr('data-cover-url');
    var player = cyberplayer("playcontainer").setup({
        width: '100%',
        height: '100%',
        file: videourl,
        image: cover_url,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        tokenEncrypt: true,
        // AccessKey
        ak: '16e1df1478ab483f887311919b9d8fbb'
    });
    player.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        xfzajax.get({
            // 获取token的url
            'url': '/course/course_token/',
            'data': {
                'video': videourl
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    player.setToken(e.file, token);
                } else {
                    alert('token错误！');
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
};
CourseDetail.prototype.run =function () {
    this.initPlayVideo();
};
$(function () {
   var course = new CourseDetail();
   course.run();
});