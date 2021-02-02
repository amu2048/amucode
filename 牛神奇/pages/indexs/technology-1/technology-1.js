// pages/indexs/technology-1/technology-1.js
Page({
  data: {
    url:'http://www.nongcun5.net/yangzhi/201903/02165.html',
  },
 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
    // var dataurl = options.dataurl;
   var dataurl =  JSON.parse(decodeURIComponent(options.dataurl));
    console.log("文章详情即将访问的url是"+dataurl.url)
    this.setData({
      url: dataurl.url
    });
  }
})