// pages/myme/myme.js//获取应用实例
var INTERFACES = require('../../../utils/interfaceUrls.js');
const app = getApp();
Page({
  data: {
    userInfo: '',
    openid:'',
    hasUserInfo: 'true'
  },
  tomessagelist:function(){
    var that =this;
    console.log("跳转我的帖子id:"+that.data.openid)
    app.globalData.myluntan = app.globalData.openid
    wx.switchTab({
      url: '../../luntan/Messagelist/Messagelist',
    })
  },
  onLoad: function () {
    var that = this;
    //如果没有openid就把我的页面hasUserInfo值假 显示微信登录按钮
    if (app.globalData.openid != '') {
      that.setData({
        userInfo: app.globalData.userInfo,
        openid :app.globalData.openid,
        hasUserInfo: false,
      });
      console.log("我的界面获取全局变量openid"+that.data.openid)
    }
  },
  //用户点击微信登录按钮触发获取用户信息
  bindGetUserInfo: function (e) {
    if (e.detail.userInfo) {
      //用户按了允许授权按钮
      var that = this;
      app.globalData.userInfo = e.detail.userInfo;
      that.setData({
        userInfo: e.detail.userInfo,
        hasUserInfo: false,
      });
      wx.login({
        success: res => {
          console.log("登录微信获取code", res.code);
          app.globalData.code = res.code;
          var da = {};
            da.code = res.code,
            console.log("opid请求接口的code1", that.data.usercode);
            da.nickName = that.data.userInfo.nickName,
            da.avatarUrl = that.data.userInfo.avatarUrl,
            da.gender = that.data.userInfo.gender,
            da.country = that.data.userInfo.country,
            da.province = that.data.userInfo.province,
            da.citys = that.data.userInfo.city,
            wx.request({
              url: INTERFACES.getopenid, //调用INTERFACES中的注册登录接口
              data: da,
              header: {
                'content-type': 'application/x-www-form-urlencoded',
                "dataType": "json"
              },
              method: "POST",
              success: function (res) {
                app.globalData.openid = res.data.openid
                //微信授权成功进入我的页
                wx.switchTab({
                  url: '../mymes/mymes'
                })
              }
            });
          wx.getSetting({
            success: function (res) {
              if (res.authSetting['scope.userInfo']) {
                console.log("已经授权");
                wx.switchTab({
                  url: '../mymes/mymes'
                })
              }
            }
          })
        }
      });
    } else {
      //用户按了拒绝按钮
      wx.showModal({
        title: '警告',
        content: '您点击了拒绝授权，将无法进入小程序，请授权之后再进入!!!',
        showCancel: false,
        confirmText: '返回授权',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击了“返回授权”')
          }
        }
      })
    }
  },
  // 事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onShow: function () {}
})