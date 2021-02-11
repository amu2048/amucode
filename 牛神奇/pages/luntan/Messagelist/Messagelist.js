var INTERFACES = require('../../../utils/interfaceUrls.js');
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    datas: {},
    requesedata:'',
    select_val: '',
  },
  //搜索函数
  search:function(event){
    var that = this;
    console.log("搜索内容为："+ event.detail.value)
    var search = event.detail.value
    wx.request({
      url: INTERFACES.luntansearch, //调用INTERFACES中的获取搜索供求信息接口,
      data: {search:search},
      method: "POST",
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success(res) {
        if(res.data[0].select_val == ''){
          that.setData({
            datas:'',
            select_val: res.data[0].select_val
          })
        }else{
          that.setData({
            datas: res.data,
            select_val: res.data[0].select_val
          })
        } 
      },
      fail: function() {
        that.setData({
          datas:'',
          select_val: res.data[0].select_val
        })
      }
    })
  },


//拨打电话
  boda: function (e) {
    wx.makePhoneCall({
      phoneNumber: e.target.id
    })
  },
//预览图片
  bindtap_img: function (e) {
    wx.previewImage({
      current: e.target.id,
      urls: [e.target.id]
    })
  },
//去发布跳转
  tofabu: function () {
    wx.switchTab({
      url: '/pages/fabu1/fabu/fabu',
    })
  },
//获取点赞数
  dianzanshu: function () {
    var that = this;
    wx.request({
      url: INTERFACES.like, //调用INTERFACES中的获取供求信息的点赞数和评论数接口,
      method: "POST",
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success(res) {
        that.setData({
          dianzanshu: res.data
        })
      }
    })
  },
  //获取供求信息
  datas:function(){
    var that =this;
    if(app.globalData.myluntan !=''){
      that.setData({
        requesedata:app.globalData.myluntan
      })
    }
    wx.request({
      url: INTERFACES.getmessage, //调用INTERFACES中的获取供求信息接口,
      data:{myopenid:that.data.requesedata},
      method: "POST",
      header: {
        //'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success(res) {
        app.globalData.myluntan='';
        that.setData({
          requesedata:''
        })
        if(res.data[0].select_val == ''){
          that.setData({
            datas:'',
            select_val: res.data[0].select_val
          })
        }else{
          that.setData({
            datas: res.data,
            select_val: res.data[0].select_val
          })
        } 
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    if(app.globalData.myluntan !=''){
      that.setData({
        requesedata:app.globalData.myluntan
      })
    }
    wx.showLoading({
      title: '加载中',
    })
    //that.dianzanshu();
    console.log("论坛列表数据的初始请求data" + that.data.requesedata)
    wx.request({
      url: INTERFACES.getmessage, //调用INTERFACES中的获取供求信息接口,
      data: {myopenid:that.data.requesedata},
      method: "POST",
      header: {
        //'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success(res) {
        app.globalData.myluntan='';
        that.setData({
          requesedata:''
        })
        if(res.data[0].select_val == ''){
          that.setData({
            datas:'',
            select_val: res.data[0].select_val
          })
        }else{
          that.setData({
            datas: res.data,
            select_val: res.data[0].select_val
          })
        } 
      },fail: function () {
        wx.showToast({
          icon: 'none',
          title: "刷新失败，请重进界面",
        })
      }
    }),
    
    setTimeout(function () {
      wx.hideLoading()
    }, 2000)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this;
    that.datas(); //获取供求信息
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function (res) {
    if (res.from === 'button') {
      return {
        title: res.target.dataset.title,
        path: 'pages/index4/index4?id=' + JSON.stringify(res.target.id),
      }
    }
    return {
      path: 'pages/index/index',
    }

  }
})