var INTERFACES = require('../../utils/interfaceUrls.js');
var app = getApp();

Page({
  data: {
    userInfo: '',
    usercode: '',
    //判断小程序的API，回调，参数，组件等是否在当前版本可用。
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
 
  onLoad: function () {
    var that = this;
    // 查看是否授权
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          console.log("onload函数 已经授权");
          wx.getUserInfo({
            success: function (res) {
              console.log("获取用户信息", res.userInfo);
              // 我这里实现的是在用户授权成功后，调用微信的 wx.login 接口，从而获取code
              app.globalData.userInfo = res.userInfo;
              wx.login({
                success: res => {
                  console.log("登录微信获取code", res.code);
                  app.globalData.code = res.code;
                }
              });
              //用户已经授权过
              wx.switchTab({
                url: '/pages/indexs/index/index'
              })
            },
            fall: function () {
              wx.showModal({
                title: '提醒',
                content: '尚未进行授权，请点击确定跳转到授权页面进行授权。',
                success: function (res) {
                  wx.navigateTo({
                    url: '../login/login',
                  })
                }
              });
            }
          });
        }
      }
    })
  },
  //获取opid
  get_openid: function(){
    var that = this;
    var da = {};
      da.code =  that.data.usercode,
      console.log("opid请求接口的code1",  that.data.usercode);
      da.nickNamee = that.data.userInfo.nickName,
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
            
            app.globalData.openid = res.data.openid;
            console.log("插入小程序登录用户信息成功！");
            //登录注册成功后,跳转进入小程序首页
            wx.switchTab({
              url: '/pages/indexs/index/index'
            })
            
          }
        });
  },
  //点击授权按钮
  bindGetUserInfo: function (e) {
    if (e.detail.userInfo) {
      //用户按了允许授权按钮
      var that = this;
      app.globalData.userInfo = e.detail.userInfo
      that.setData({
        userInfo: e.detail.userInfo
      });
      wx.login({
        success: res => {
         
          app.globalData.code = res.code;
          that.setData({
            usercode: res.code
          });
          var da = {};
          da.code =  res.code,
          console.log("opid请求接口的code1",  that.data.usercode);
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
                //登录注册成功后,跳转进入小程序首页
                wx.switchTab({
                  url: '/pages/indexs/index/index'
                })
                
              }
            });
          wx.getSetting({
            success: function (res) {
              if (res.authSetting['scope.userInfo']) {
                console.log("已经授权");
                  wx.switchTab({
                  url: '/pages/indexs/index/index'
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
  
  onShow: function () {
    //是否授权
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          console.log("已经授权");
            wx.switchTab({
            url: '/pages/indexs/index/index'
          })
        }
      }
    })
  }

})