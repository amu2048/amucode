//获取应用实例
var INTERFACES = require('../../../utils/interfaceUrls.js');
var app = getApp();
var cardTeams;
Page({
  data: {
    items: [{
      "viewid": "1",
      "imgsrc": "http://i.nongcun5.net/file/upload/201903/02/21-36-18-46326-1.jpg",
      "url": "http://www.nongcun5.net/yangzhi/201903/02165.html",
      "watch":"56775687",
      "like": "87877",
      "pinglun":"14256",
      "title": "肉牛养殖的注意事项",
      "desc": "肉牛养殖的注意事项",
    }, {
      "viewid": "2",
        "imgsrc": "http://i.nongcun5.net/file/upload/201903/02/21-38-01-46397-1.jpg",
        "url": "http://www.nongcun5.net/yangzhi/201903/02165.html",
        "watch":"43667",
        "like": "77342",
        "pinglun":"12345",
        "title": "牛拉稀怎么办",
        "desc": "牛拉稀怎么办",
    }, {
      "viewid": "3",
        "imgsrc": "http://i.nongcun5.net/file/upload/201903/02/21-32-36-46006-1.jpg",
        "url": "http://www.nongcun5.net/yangzhi/201903/0292.html",
        "watch":"855634",
        "like": "6662",
        "pinglun":"19634",
        "title": "肉牛亚硝酸盐中毒病因及防治措施",
        "desc": "肉牛亚硝酸盐中毒病因及防治措施",
    }, {
      "viewid": "4",
        "imgsrc": "http://i.nongcun5.net/file/upload/201903/02/21-34-20-46144-1.jpg",
        "url": "http://www.nongcun5.net/yangzhi/201903/02154.html",
        "watch":"56757",
        "like": "234234",
        "pinglun":"165765",
        "title": "黄牛高产养殖技术",
        "desc": "黄牛高产养殖技术",
    },
    {
      "viewid": "5",
        "imgsrc": "http://i.nongcun5.net/file/upload/201903/02/21-38-01-46397-1.jpg",
        "url": "http://www.nongcun5.net/yangzhi/201903/02194.html",
        "watch":"2667475",
        "like": "234324",
        "pinglun":"18577",
        "title": "牛为什么只吃不长",
        "desc": "牛为什么只吃不长",
    },
    ]
  },
  toDetail:function(e){
    var dataurl={}
    dataurl.url= e.currentTarget.dataset.url;
    console.log("dataurl:"+dataurl)
      wx.navigateTo({
        url: "../technology-1/technology-1?dataurl="+ encodeURIComponent(JSON.stringify(dataurl)),
      })
  },
  onLoad: function () { 
    var that = this;
   // console.log('onLoad:' + app.globalData.domain)
   wx.request({
    url: INTERFACES.technology, //调用INTERFACES中的文章列表接口
    data: {"page":1},
    method: "post",
    header: {
      'content-type': 'application/x-www-form-urlencoded',
      "dataType": "json"
    },
    success: function (res) {
      console.log('返回数据',res.data.items)
      if (res.data.items) {
        that.setData({
          items: res.data.items
        });
    
      } else {
        wx.showModal({
          title: '提示',
          content: '获取数据失败!',
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
        content: '网络失败!',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
          }
        }
      });
    }
  });
  }
})