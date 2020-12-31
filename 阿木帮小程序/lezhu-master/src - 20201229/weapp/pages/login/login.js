// pages/login.js
var INTERFACES = require('../../util/interfaceUrls.js');
var app=getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  //调用登录注册接口
  sendReq:function(user){
    console.log('登录接口调用');
    //发送请求 获取需求列表 传参： type需求类型 urgent是否紧急任务
    var that = this;
    var reqData={};
    reqData.userId=user.nickName;
    reqData.userUrl=user.avatarUrl;
    reqData.gender=user.gender;
    reqData.province=user.province;
    reqData.city=user.city;
    reqData.country=user.country;
    wx.request({
    url: INTERFACES.login,
    data: reqData,
    method:"POST",
    header: {
     // 'content-type': 'application/json',
      'content-type': 'application/x-www-form-urlencoded',
      "dataType":"json"
    },
    success: function(res) {
        if (res.data.length == 0){
          console.log('登录接口返回空值');
          wx.navigateBack({ 
            delta: 1, })
        }
        
      },
      fail: function() {
          that.setData({
            array:app.mockHelpList
          });
      }
      })
    },
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },
    bindGetUserInfo: function(e){
      var that = this;
      //此处授权得到userInfo
      console.log('获取授权信息',e.detail.userInfo);
      var user = e.detail.userInfo;
      //接下来写业务代码
      app.globalData.userInfo = user;
      console.log('开始发送登录接口请求');
      that.sendReq(user);
      console.log('进入返回列表界面');
      // wx.redirectTo({ 
        
      //   url: '../helpList/helpList',
      //   success: function (res) { 
      //   // success 
      //   }
      //   }) 
      //最后，记得返回刚才的页面
      wx.navigateBack({
        url: '../helpList/helpList'
      })

   },
 

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },


})