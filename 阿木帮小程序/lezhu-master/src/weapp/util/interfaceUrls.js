var prefix = {
    "develop":"http://127.0.0.1:2048/",
    "test":"https://we.amuqitan.cn/",
    "produce":"https://weapp.zhanghao90.cn/intl-console-web/user/"
}
["test"];

module.exports = {
    //helpList获取帮助信息列表
    "searchServiceNeeded":prefix + "searchServiceNeeded",
    //myPage
    "getUserInfo":prefix + "getUserInfo",
    //helpDetail确认领取任务
    "acceptRequest":prefix + "acceptRequest",
    //helpInput添加求助信息
    "postNeed":prefix + "postNeed",
    //myToHelp
    "searchMyService":prefix + "searchMyService",
    //myGetHelp
    "searchMyNeed":prefix + "searchMyNeed",
    //确认他帮助
    "Confirmhelp":prefix + "Confirmhelp",
    //否认他帮助
    "noConfirmhelp":prefix + "noConfirmhelp",
    //确认帮助 悬赏积分
    "confirmServiceComplete":prefix + "confirmServiceComplete",
    //取消求助信息
    "cancelhelp":prefix + "cancelhelp",
    //登录注册
     "login":prefix + "login"
};