// pages/luntan/Messagelists/Messagelists.js
var INTERFACES = require('../../../utils/interfaceUrls.js');
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

    if_del_val: false,
    if_guanbi: false,
    hui_guan: false,
    ly_size: '这是评论数',
    ifzan: null,
    datas: {
      // "36": {
      //   "liulanliang": "9999",
      //   "username": "amu",
      //   "userimg":"",
      //   "times": "amu1",
      //   "haoma": "1310431794",
      //   "id": "36",
      //   "select_val": "类型1",
      //   "neirong": "这是测试数据第一条",
      //   "imgurl_01": "20210205093310_36.png",
      //   "dizhi": "南京大陆699号"
      // }
    },
    huifus: "回复数"
  },
  //点赞
  dianzan: function () {
    var that = this;
    wx.request({
      url: INTERFACES.ifdianzan, //调用INTERFACES中的获取供求信息接口详细信息
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      method: "POST",
      data: {
        useropenid: that.data.openid,
        messageid: that.data.idx,
        ifdianzan: that.data.ifzan
      },
      success(res) {
        that.setData({
          ifzan: res.data
        })
        //  wx.navigateTo({
        //    url: '../Messagelists/Messagelists?id='+that.data.idx,
        //  })
      }
    })

  },
  select_del: function () {
    this.setData({
      if_del_val: !this.data.if_del_val
    })
  },
  //删除自己的文章
  del: function () {
    console.log("进入删除文章函数");
    var that = this;
    
    wx.showModal({
      title: '提示',
      content: "确定删除",
      success(res) {
        if (res.confirm) {
          console.log("用户确认删除"),
            wx.request({
              url: INTERFACES.delmessage, //调用INTERFACES中的获取供求信息接口详细信息
              header: {
                'content-type': 'application/x-www-form-urlencoded',
                "dataType": "json"
              },
              method: "POST",
              data: {
                delid: that.data.idx,
                openid: that.data.openid
              },
              success(res) {
                wx.showToast({
                  icon: 'success',
                  title: "删除成功",
                })
                setTimeout(function () {
                  wx.switchTab({
                    url: '../Messagelist/Messagelist',
                  })
                }, 2200)
              }
            })
        } else if (res.cancel) {

        }
      }
    })
  },
  //点击举报按钮触发
  jbao: function () {
    var that = this;
    wx.showModal({
      title: '提示',
      content: "确定举报",
      success(res) {
        if (res.confirm) {
          wx.showToast({
            icon: 'success',
            title: "举报成功",
          })
        }
      }
    })
  },
  //点击首页返回到首页
  shouye: function () {
    wx.switchTab({
      url: '/pages/indexs/index/index',
    })
  },
  //点击联系他 拨打电话
  boda: function (e) {
    wx.makePhoneCall({
      phoneNumber: e.currentTarget.id
    })
  },
  //展示图片
  bindtap_img: function (e) {
    wx.previewImage({
      current: e.target.id,
      urls: [e.target.id]
    })
  },

  // 获取用户信息存放在发布消息的data中
  get_globaldata: function () {
    var that = this;

    that.setData({
      openid: app.globalData.openid,
    });
    console.log("把全局变量数据写入初始data中" + that.data.openid);
  },

  ping_guan: function (options) {
    this.setData({
      ping_placeholder: this.data.pingls + options.currentTarget.dataset.ping,
      if_guanbi: !this.data.if_guanbi
    })
  },
  //发送评论
  ping_form: function (e) {
    var that = this;
    if (that.data.name == undefined) {
      wx.showToast({
        icon: 'none',
        title: "请先登录",
      })
    } else {
      wx.request({
        url: that.data.request_url + '/wx/pinglun.php',
        header: {
          'content-type': 'application/json'
        },
        data: {
          ping_idx: that.data.idx,
          useame_01: that.data.name,
          ping_hui: that.data.pingls,
          useame_02: '',
          ping_val: e.detail.value.ping_txt,
          hui_val: '',
        },
        success(res) {
          that.setData({
            ping_val: res.data,
            if_guanbi: false,
          })
        }
      })
    }
  },

  useame: function (options) {
    var that = this;
    that.setData({
      ping_placeholders: options.currentTarget.dataset.hui_useame,
      hui_name: options.currentTarget.dataset.hui,
      ping_placeholder: that.data.huifus + options.currentTarget.dataset.hui_useame,
      hui_guan: !that.data.hui_guan,
    })
  },
  hui_guan: function () {
    this.setData({
      hui_guan: !this.data.hui_guan,
    })
  },

  hui_form: function (e) {
    var that = this;
    if (that.data.name == undefined) {
      wx.showToast({
        icon: 'none',
        title: "请先登录",
      })
    } else {
      wx.request({
        url: that.data.request_url + '/wx/pinglun.php',
        header: {
          'content-type': 'application/json'
        },
        data: {
          ping_idx: that.data.idx,
          useame_01: that.data.name,
          ping_hui: that.data.huifus,
          useame_02: that.data.hui_name,
          ping_val: '',
          hui_val: e.detail.value.hui_txt,
        },
        success(res) {
          that.setData({
            ping_val: res.data,
            hui_guan: !that.data.hui_guan,
          })
        }
      })
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;

    that.setData({
      openid: app.globalData.openid
    });
    console.log("把全局变量数据写入初始data中" + that.data.openid); //保存用户信息
    that.setData({
      idx: options.id
    });
    var id = JSON.parse(options.id);
    wx.request({
      url: INTERFACES.getmessages, //调用INTERFACES中的获取供求信息接口详细信息
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      method: "POST",
      data: {
        id: id,
        openid: that.data.openid
      },
      success(res) {
        console.log("获取是否点赞：" + res.data[0].dianzan_off)
        that.setData({
          datas: res.data,
          ifzan: res.data[0].dianzan_off
        })
      }
    })

    // wx.request({
    //   url: that.data.request_url + '/wx/liulan_val.php',
    //   header: {
    //     'content-type': 'application/json'
    //   },
    //   data: {
    //     idx: id
    //   },
    //   success(res) {
    //     that.setData({
    //       liulan: res.data
    //     })
    //   }
    // })

    // wx.request({
    //   url: that.data.request_url + '/wx/pinglun.php',
    //   header: {
    //     'content-type': 'application/json'
    //   },
    //   success(res) {
    //     that.setData({
    //       ping_val: res.data,
    //     })
    //   }
    // })

    // wx.request({
    //   url: that.data.request_url + '/wx/pinglun_size.php',
    //   header: {
    //     'content-type': 'application/json'
    //   },
    //   data: {
    //     ly_size: options.id
    //   },
    //   success(res) {
    //     that.setData({
    //       ly_size: res.data
    //     })
    //   }
    // })

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