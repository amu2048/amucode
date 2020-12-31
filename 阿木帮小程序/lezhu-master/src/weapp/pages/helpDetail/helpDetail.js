var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
  data: {
    wechatUserInfo:{},
    latitude: null,
    longitude: null,
    location:null,
    headIcon:null,
    nickName:null,
    payScore:null,
    title:"",
    content:"",
    taskId:"",
    markers: [
  
    ],
    covers: [

    ]
    
  },
  //点击立即帮助时出发函数 提交申请帮助
  helpClick:function(){
     var that = this;
        wx.showModal({
          title: '是否揭榜',
          content: '请尽快与发布者联系！',
          success: function(res) {
            if (res.confirm) {
              that.sendReq();
            }
          }
        })
  },
  //发送请求 请求发布者确认 任务人
  sendReq:function(){
    //发送请求
    var that = this;
    var reqData={};
    reqData.taskId=that.data.taskId;
    reqData.helperId=that.data.wechatUserInfo.nickName;
    reqData.helpUrl=that.data.wechatUserInfo.avatarUrl;

    wx.request({
    url: INTERFACES.acceptRequest,
    method:"POST",
    data: reqData,
    header: {
        'content-type': 'application/x-www-form-urlencoded',
        "dataType":"json"
    },
    success: function(res) {
        if(res.data.status){
            if(res.data.status==0){
              wx.navigateTo({
                url: '../helpConfirmed/helpConfirmed?mobile='+res.data.mobile
              })
            }
            else if(res.data.status==1){
                wx.showModal({
                      title: '提示',
                      content: '确认失败',
                      success: function(res) {
                        if (res.confirm) {
                            console.log('用户点击确定')
                        }
                      }
                });
            }
        }
        else{
            wx.redirectTo({
              url: '../helpConfirmed/helpConfirmed?mobile=13800000000'
            })
        }
    },
    fail: function() {
      wx.redirectTo({
        url: '../helpConfirmed/helpConfirmed?mobile=13800000000'
      })
    }
    })
  },
  onLoad: function () {
    var that = this
  	//调用应用实例的方法获取全局数据
    that.setData({
      latitude:app.mapData.latitude,
      longitude:app.mapData.longitude,
      location:app.mapData.location,
      headIcon:app.mapData.headIcon,
      nickName:app.mapData.nickName,
      payScore:app.mapData.payScore,
      title:app.mapData.title,
      content:app.mapData.content,
      taskId:app.mapData.taskId,
      markers: [{
        id: 1,
        latitude:app.mapData.latitude,
        longitude:app.mapData.longitude,
        name:app.mapData.location,
      }],
      covers: [{
        latitude:app.mapData.latitude,
        longitude:app.mapData.longitude,
        iconPath: '../image/map-location.png'
      }]
    });
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
        //更新数据
        that.setData({
            wechatUserInfo:userInfo
        });
        that.update();
    })
  }
})