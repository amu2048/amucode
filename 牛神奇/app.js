// app.js
var INTERFACES = require('/utils/interfaceUrls.js');
App({
  //获取opid
  get_openid: function () {
    console.log("app.js--get_openid")
    var that = this;
    var da = {};
    wx.login({
      success: res => {
        that.globalData.code = res.code,
        console.log("opid请求接口的code1", that.globalData.code),
          da.code = res.code,
          da.nickName = that.globalData.userInfo.nickName,
          da.avatarUrl = that.globalData.userInfo.avatarUrl,
          da.gender = that.globalData.userInfo.gender,
          da.country = that.globalData.userInfo.country,
          da.province = that.globalData.userInfo.province,
          da.citys = that.globalData.userInfo.city,
          wx.request({
            url: INTERFACES.getopenid, //调用INTERFACES中的注册登录接口
            data: da,
            header: {
              'content-type': 'application/x-www-form-urlencoded',
              "dataType": "json"
            },
            method: "POST",
            success: function (res) {
              that.globalData.openid = res.openid
              console.log("插入小程序登录用户信息成功！");
              //登录注册成功后,跳转进入小程序首页
              wx.switchTab({
                url: '/pages/indexs/index/index'
              })

            }
          });
        console.log("app.js中已授权--获取用户信息--登录微信获取 that.globalData.code", that.globalData.code);
      }
    });

  },
  onLaunch() {
    var that = this;
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now());
    wx.setStorageSync('logs', logs);
    // if (this.globalData.userInfo && this.globalData.code != '') {
    //如果用户授权则获取用户信息存在全局变量
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          console.log("onload函数 已经授权"),
            // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
            wx.getUserInfo({
              lang: "zh_CN",
              //success: res => {
              success: function (res) {
                // 把用户基本信息储存再全局变量中
                that.globalData.userInfo = res.userInfo,
                  console.log("app.js中已授权--获取用户信息--把用户信息存到globaldata中：" + that.globalData.userInfo.city);

                //获取openid存入全局
                that.get_openid();
                // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回,所以此处加入 callback 以防止这种情况
                if (that.userInfoReadyCallback) {
                  that.userInfoReadyCallback(res)
                };
                //已经授权则直接打开首页
                wx.switchTab({
                  url: '/pages/indexs/index/index'
                })
              }
            });

        } else {
          //用户未授权引导去登录
          wx.navigateTo({
            url: '/pages/login/login',
          })
        }
      }
    })
  },
  globalData: {
    userInfo: '',
    code: '',
    openid: ''
  }
})