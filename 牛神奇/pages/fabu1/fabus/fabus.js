var QQMapWX = require('../../../utils/qqmap-wx-jssdk.js');
var qqmapsdk;
var INTERFACES = require('../../../utils/interfaceUrls.js');
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    imagurl: [],
    imageList: [],
    select_if: true,
    userimg: '',
    username: '',
    content_up_del_if: false,
    select_val: null,

  },
  // 获取用户信息存放在发布消息的data中
  get_globaldata: function () {
    var that = this;
    console.log("把全局变量数据写入初始data中")
    that.setData({
      userimg: app.globalData.userInfo.avatarUrl,
      username: app.globalData.userInfo.nickName,
    });
  },
  //添加图片或者拍照添加
  select_img: function () {
    var that = this;
    //删除imgurl内的所有图片和请求删除图片文件接口
    for (var i = 0; i < that.data.imagurl.length; i++) {
      console.log("开始清空imagurl内数据和后台文件")
      wx.request({
        url: INTERFACES.delimg, //发布消息接口
        data: {
          "delimgname": that.data.imagurl[i]
        },
        method: "POST",
        header: {
          'content-type': 'application/x-www-form-urlencoded',
          "dataType": "json"
        },
        success(res) {
          console.log("已经清空所有imagurl内的后台图片文件")
          that.setData({
            imagurl:that.data.imagurl.splice(i, 1),
          })
        }
      })
    };
    var imageList = that.data.imageList;
    wx.chooseImage({
      count: 6,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        var imgurl = res.tempFilePaths;
        var imgarry = imageList.concat(imgurl);
        that.up_img(imgarry);
        that.setData({
          imageList: imgarry
        })
        if (that.data.imageList.length == 6) {
          that.setData({
            select_if: false
          })
        }
      }

    })

  },
  //删除照片判断逻辑
  remove_img: function (imageList, del_imgs) {
    var that = this;

    for (var i = 0; i < imageList.length; i++) {
      if (imageList[i] == del_imgs) {
        var delimgname = that.data.imagurl[i];
        imageList.splice(i, 1);
        that.data.imagurl.splice(i, 1);

        wx.request({
          url: INTERFACES.delimg, //发布消息接口
          data: {
            "delimgname": delimgname
          },
          method: "POST",
          header: {
            'content-type': 'application/x-www-form-urlencoded',
            "dataType": "json"
          },
          success(res) {
            console.log("删除图片成功开始删除显示")
          }
        });
      }
    }

    return -1;
  },
  //删除照片按钮
  del_imgs: function (e) {

    var imageList = this.data.imageList;
    var del_imgs = e.target.id;
    this.remove_img(imageList, del_imgs);
    this.setData({
      content_up_del_if: false,
      imageList: this.data.imageList,
      imagurl: this.data.imagurl,
    });

    if (this.data.imageList.length < 6) {
      this.setData({
        select_if: true
      })
    }
  },
  //点击图片按放大预览图片
  yulian_select_img: function (e) {
    wx.previewImage({
      current: e.target.id,
      urls: [e.target.id]
    })
  },
  //获得地址
  dizhi: function () {
    var that = this;

    wx.chooseLocation({
      type: 'wgs84',
      success(res) {
        var name = res.name
        var address = res.address
        that.setData({
          address: address
        })
      },
      fail() {

      }
    })
    if (that.data.address == undefined) {
      wx: wx.showModal({
        title: '提示',
        content: "请开启位置授权",
      })
    }
  },
  //内部使用获取列表中的图片
  huoqu_img: function (str) {
    var indexOf = str.lastIndexOf("\/");
    str = str.substring(indexOf + 1, str.length);
    return str;
  },
  //上传图片
  // up_img: function (cb = function(){}) {
  up_img: function (e) {
    var that = this;
    console.log("进入upimg接口函数1" + that.data.imageList);
    // var imageList = that.data.imageList;
    var imageList = e;
    for (var i = 0; i < imageList.length; i++) {
      console.log("进入upimg接口for函数");
      var data = {}
      data.imgid = i;
      wx.uploadFile({
        url: INTERFACES.upimg, //调用INTERFACES中的上传图片接口
        filePath: String(imageList[i]),
        formData: data,
        name: 'img',
        header: {
          "Content-Type": "multipart/form-data"
        },
        success: function (e) {
          console.log("图片上传成功", e);
          var url = that.data.imagurl.concat(e.data);
          that.setData({
            //把图片上传的地址存进去
            imagurl: url
          })
        }
      })
    }

  },

  postmess: function (e) {
    console.log("进入post消息接口");
    var that = this;
    console.log("进入post时data中的omgurl" + that.data.imageListurl)
    wx.request({
      url: INTERFACES.newsrelease, //发布消息接口
      data: {
        userimg: that.data.userimg,
        username: that.data.username,
        openid: app.globalData.openid,
        select_val: that.data.select_val,
        title: e.detail.value.title,
        neirong: e.detail.value.textarea,
        dizhi: that.data.address,
        haoma: e.detail.value.dianhua,
        imgurl_01: that.data.imagurl[0],
        imgurl_02: that.data.imagurl[1],
        imgurl_03: that.data.imagurl[2],
        imgurl_04: that.data.imagurl[3],
        imgurl_05: that.data.imagurl[4],
        imgurl_06: that.data.imagurl[5],
      },
      method: "POST",
      header: {
        //'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success(res) {
        that.setData({
          textarea_val: '',
          dianhua_val: '',
          imageList: [],
        })
        wx.showToast({
          icon: 'success',
          title: "发布成功",
        })
        setTimeout(function () {
          wx.switchTab({
            url: '/pages/luntan/Messagelist/Messagelist',
          })
        }, 2300)
      }
    })
  },
  //触发发布消息按钮
  formSubmit: function (e) {
    var that = this;
    console.log("from表单信息" + e.detail.value.title + e.detail.value.textarea + that.data.imageListurl);
    if (e.detail.value.textarea !== '') {
      var zhengze = /^[1][3,4,5,7,8][0-9]{9}$/; //电话号正则筛选
      var phone = e.detail.value.dianhua;
      if (!zhengze.test(phone)) {
        wx.showToast({
          icon: 'none',
          title: "请输入手机号码",
        })
      } else {
        if (that.data.username == '') {
          wx.showToast({
            icon: 'none',
            title: "请先登录账号",
          })
        } else {
          that.postmess(e)
        }
      }
    } else {
      wx.showToast({
        icon: 'none',
        title: "消息内容不能为空",
      })
    }
  },

  //获取地址
  getLocation: function () {
    var that = this
    wx.getLocation({
      type: 'wgs84',
      success: function (res) {
        var speed = res.speed
        var accuracy = res.accuracy
        var latitude = res.latitude
        var longitude = res.longitude
        that.setData({
          latitude: res.latitude,
          longitude: res.longitude
        })

        var qqmapsdk = new QQMapWX({
          key: 'S76BZ-YV3WW-4F2RR-RWQ4H-VFTHE-FTFKN' //key
        });

        qqmapsdk.reverseGeocoder({
          location: {
            latitude: res.latitude,
            longitude: res.longitude
          },
          success: function (res) {
            that.setData({
              address: res.result.address
            })
          }
        })
      },
      fail: function () {

      }
    })
  },



  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    console.log("获取类别值" + options.select_val)
    that.setData({
      select_val: options.select_val
    });
    that.get_globaldata();
    that.getLocation()

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