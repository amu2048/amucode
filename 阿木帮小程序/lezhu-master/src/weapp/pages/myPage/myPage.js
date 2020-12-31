var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
    data: {
        wechatUserInfo: {},
        userInfo:{}
    },
    onLoad: function () {
        console.log('MY页的onLoad')
        var that = this
        //调用应用实例的方法获取全局数据
      app.getUserInfo(function(userInfo){
          //更新数据
          that.setData({
              wechatUserInfo:userInfo
          });
          that.update();
      })
      console.log('我的获取全局登录信息更新后wechatUserInfo',that.data.wechatUserInfo)
  },
    onReady: function () {
    
        this.fetchData();
    },

    onShow:function(){
       
        this.fetchData();
    },

    //获取个人信息 我的积分数据
    fetchData:function(){
        console.log('MY页的fetchData')
        var that = this;
        var da={}
        da.userId=that.data.wechatUserInfo.nickName;
        //da.userId=app.globalData.userInfo.nickName;
        console.log('MY界面fetchData中的wechatUserInfo数据是',that.data.wechatUserInfo)
        wx.request({
            url: INTERFACES.getUserInfo,
            header:{
                'content-type': 'application/x-www-form-urlencoded',
                "dataType":"json"
            },
            data:da,
            method:"POST",
            success: function(resp) {
                if (resp.data.usePoint){
                    that.setData({
                        userInfo:resp.data
                    });
                }
                else{
                    that.doMock();
                }
            },
            fail:function(resp){
                that.doMock();
            }
        });
    },

    doMock:function(){
        this.setData({
            userInfo:app.mockUserInfo
        });
    },

    //跳转页面
    myToHelpPage:function(){
        wx.navigateTo({
             url: '../myToHelp/myToHelp'
        })
    },
    
    myGetHelpPage:function(){
        wx.navigateTo({
             url: '../myGetHelp/myGetHelp'
        })
    }
})