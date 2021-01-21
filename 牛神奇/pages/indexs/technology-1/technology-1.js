// pages/indexs/technology-1/technology-1.js
Page({
  data: {
    url:'http://www.nongcun5.net/yangzhi/201903/02165.html',
  },
 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
    var dataurl = options.dataurl;
    console.log("url是"+dataurl)
    this.setData({
      url: dataurl
    });
  }
})