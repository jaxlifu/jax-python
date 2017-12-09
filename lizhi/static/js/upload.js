function upload() {
    var name = document.getElementsByName('name')[0].value
    var mobile = document.getElementsByName('mobile')[0].value
    var number = document.getElementsByName('number')[0].value
    var message = document.getElementsByName('message')[0].value
    var image_school = document.getElementsByName('image_school')[0].value
    var image_current = document.getElementsByName('image_current')[0].value
    var image_meeting = document.getElementsByName('image_meeting')[0].value
    var from = document.getElementById('upload')





    if (!name) {
        alert("请输入姓名!")
        return
    }
    if (!mobile) {
        alert("请输入手机号")
        return
    }
    var reg = /^1[3|4|5|7|8][0-9]{9}$/ //验证规则
    if (!reg.test(mobile)) {
        alert("请输入正确的手机号")
        return
    }
    if (!number) {
        alert("请输入学号")
        return
    }
    if (!message) {
        alert("请输入毕业感言")
        return
    }
    if (!image_school) {
        alert("请上传你的在校照片")
        return
    }
    if (!image_current) {
        alert("请上传近期照片")
        return
    }

    from.submit()
}
