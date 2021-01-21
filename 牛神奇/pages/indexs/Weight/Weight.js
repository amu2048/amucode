// pages/Weight/Weight.js
var INTERFACES = require('../../../utils/interfaceUrls.js');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    selectShow: false, //控制下拉列表的显示隐藏，false隐藏、true显示
    selectData: ['标准', '偏胖', '偏瘦'], //下拉列表的数据
    index: 0, //选择的下拉列表下标
    tall:0,
  },
  // 点击下拉显示框
  selectTap() {
    this.setData({
      selectShow: !this.data.selectShow
    });
  },
  // 点击下拉列表
  optionTap(e) {
    let Index = e.currentTarget.dataset.index; //获取点击的下拉列表的下标
    this.setData({
      index: Index,
      selectShow: !this.data.selectShow
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },
  //估算体重
  formSubmit: function (e) {
    var that = this;
    console.log('触发估算体重函数，携带数据为：', e.detail.value)
    var formData = e.detail.value; //提交表单form获取的数据
    var reqData = {}; //请求数据
    reqData.xiongwei = formData.xiongwei; //胸围
    reqData.index = that.data.index; //肉牛体型 0正常 1胖 2瘦
    if (reqData.xiongwei == '' || 80>reqData.xiongwei || reqData.xiongwei>199) {
      wx.showModal({
        title: '提示',
        content: '胸围范围：80~199CM',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
          }
        }
      });
    }
     else {
      wx.request({
        url: INTERFACES.weightestimation, //调用INTERFACES中的体重估算接口
        data: reqData,
        method: "POST",
        header: {
          //'content-type': 'application/json',
          'content-type': 'application/x-www-form-urlencoded',
          "dataType": "json"
        },
        success: function (res) {
          if (res.data.tall) {
            that.setData({
              tall: res.data.tall
            });
        
          } else {
            wx.showModal({
              title: '提示',
              content: '体重估算失败!',
              success: function (res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                }
              }
            });
          }
        },
        fail: function () {
          wx.showModal({
            title: '提示',
            content: '提交失败!',
            success: function (res) {
              if (res.confirm) {
                console.log('用户点击确定')
              }
            }
          });
        }
      });
    }
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
  onShareAppMessage: function () {

  }
})