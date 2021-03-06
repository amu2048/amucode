var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
    data: {
        wechatUserInfo: {},
        userInfo:{}
    },

    onLoad: function () {
        var that = this
  	    //调用应用实例的方法获取全局数据
        app.getUserInfo(function(userInfo){
            //更新数据
            that.setData({
                wechatUserInfo:userInfo
            });
            that.update();
        })
    },

    onReady: function () {
        this.fetchData();
    },

    onShow:function(){
        this.fetchData();
    },

    //获取个人信息 我的积分数据
    fetchData:function(){
        var self = this;
        wx.request({
            url: INTERFACES.getUserInfo,
            header:{
                'content-type': 'application/x-www-form-urlencoded',
                "dataType":"json"
            },
            data: {
                userId: self.data.wechatUserInfo.nickName
            },
            method:"POST",
            success: function(resp) {
                if (resp.data.usePoint){
                    self.setData({
                        userInfo:resp.data
                    });
                }
                else{
                    self.doMock();
                }
            },
            fail:function(resp){
                self.doMock();
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