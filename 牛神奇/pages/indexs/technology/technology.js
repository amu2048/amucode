//获取应用实例
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
      let dataurl = e.currentTarget.dataset.url;
      wx.navigateTo({
        url: "../technology-1/technology-1?dataurl="+dataurl,
      })
  },
  onLoad: function () {
   // console.log('onLoad:' + app.globalData.domain)
  }
})