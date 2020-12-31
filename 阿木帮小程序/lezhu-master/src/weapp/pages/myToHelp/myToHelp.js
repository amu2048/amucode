var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
    data: {
        wechatUserInfo:{},
        toHelpArray:[],
        phone:"",
        hintFlag:true
    },
     //点击电话会调用手机拨打电话界面
  takePhone:function(e){
    console.log(e.currentTarget.dataset.item)
    wx.makePhoneCall({
        phoneNumber:e.currentTarget.dataset.item
})
  },
    onLoad: function () {
        var that = this
  	    //调用应用实例的方法获取全局数据
        app.getUserInfo(function(userInfo){
            //更新数据
            console.log('我帮助的userInfo',userInfo)
            that.setData({
                wechatUserInfo:userInfo
            });
            that.update();
        })
    },
    
    onReady: function () {
        this.fetchData();
    },

    //获取数据
    fetchData:function(){
        var self = this;
        wx.request({
            url: INTERFACES.searchMyService,
            header:{
                'content-type': 'application/x-www-form-urlencoded',
                "dataType":"json"
            },
            data: {
                userId: self.data.wechatUserInfo.nickName,
            },
            method:"POST",
            success: function(resp) {
                if (resp.data.length == 0){
                    self.setData({
                        hintFlag:false
                    });
                }
                else{
                    self.setData({
                        toHelpArray:resp.data
                    });
                }
            },
            fail:function(resp){
                self.doMock();
            }
        });
    },

    doMock:function(){
        this.setData({
            toHelpArray:app.mockToHelpArray
        });
    },
})