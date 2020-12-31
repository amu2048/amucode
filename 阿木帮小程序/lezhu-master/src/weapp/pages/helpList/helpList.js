var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
  data: {
    wxUserInfo: null,
    latitudeCur: null, //经度
    longitudeCur: null, //纬度
    helptype: "全部", //默认显示全部类型的需要帮助的数据
    urgent: "false",
    index: 0, //默认显示分类列表helparray中的第0个数据
    helparray: ['全部', '紧急', '取餐', '取快递', '带文件', '租房', '美食推荐', '其他'], //帮助分类类别
    array: [],
    hintFlag: true
  },
  //点击数据 触发这个程序
  openMap: function (e) {
    var infoObj = e.currentTarget.dataset;
    app.mapData.latitude = Number(infoObj.latitude);
    app.mapData.longitude = Number(infoObj.longitude);
    app.mapData.location = infoObj.location;
    console.log('记录存入数据')
    console.log(infoObj.location)
    console.log(app.mapData.location)
    app.mapData.nickName = infoObj.nickname;
    app.mapData.headIcon = infoObj.headicon;
    app.mapData.payScore = infoObj.payscore;
    app.mapData.title = infoObj.title;
    app.mapData.content = infoObj.content;
    app.mapData.taskId = infoObj.taskid;
    wx.navigateTo({
      url: '../helpDetail/helpDetail'
    })
  },
  //选择帮助类别数触犯此事件，
  bindPickerChange: function (e) {
    var that = this;
    var i = e.detail.value; //picker语法 用.detail.value来获取当前选中的索引值
    that.setData({ //重写data中的数据值
      index: i, //类别索引为当前选择的
      helptype: that.data.helparray[i] //类别名称根据根据索引下标选择显示
    });
    if (i == 1) {
      if (that.data.helptype == "紧急") {
        that.sendReq("全部", "true");
      } else {
        that.sendReq(that.data.helptype, "true");
      }
    } else {
      that.sendReq(that.data.helptype, "false");
    }
  },
  //发起请求的封装
  sendReq: function (type, urgent) {
    //发送请求 获取需求列表 传参： type需求类型 urgent是否紧急任务
    var that = this;
    var reqData = {};
    reqData.userId = that.data.wxUserInfo.nickName;
    reqData.longitude = that.data.longitudeCur;
    reqData.latitude = that.data.latitudeCur;
    reqData.srvType = type;
    reqData.urgent = urgent;

    wx.request({
      url: INTERFACES.searchServiceNeeded,
      data: reqData,
      method: "POST",
      header: {
        // 'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        "dataType": "json"
      },
      success: function (res) {
        if (res.data.length == 0) {
          that.setData({
            //如果返回的json数据长度 0  证明没搜到内容 则hintFlag标记假
            hintFlag: false,
            array: res.data
          });
        } else {
          that.setData({
            //否则就是获取到数据了 array数剧
            hintFlag: true,
            array: res.data
          });
        }
      },
      fail: function () {
        that.setData({
          array: app.mockHelpList
        });
      }
    })
  },
  //当用户第一次拒定位后再次请求授权
  openConfirm: function () {
    wx.showModal({
      content: '检测到您没打开此小程序的定位权限，是否去设置打开？',
      confirmText: "确认",
      cancelText: "取消",
      success: function (resa) {
        console.log('show日志',resa);
        //点击“确认”时打开设置页面
        if (resa.confirm) {
          console.log('用户点击确认open')
          wx.openSetting({
            //success: (res) => {}
            success (res) {
              console.log('拉起设置界面')
              res.authSetting = {
                "scope.userLocation": true
              }
            }
          })
        } else {
          console.log('用户点击取消')
        }
      }
    });
  },
  //初始化函数
  onLoad: function (options) {
    var that = this;
    //是否授权
    wx.getSetting({
        success: function (res) {
          console.log('list初始函数')
          //授权了的话 获取登录信息
          if (res.authSetting['scope.userInfo']) {
            //全局方法获取用户信息
            console.log('已授权进去全局登录')
            app.getUserInfo(function (userInfo) {
              that.setData({
                wxUserInfo: app.globalData.userInfo
              });
              that.checkFlag();
            });
          } else {
            console.log('未授权进入index')
            wx.showModal({
              title: '提醒',
              content: '尚未进行授权，请点击确定跳转到授权页面进行授权。',
              success: function (res) {
                wx.navigateTo({
                  url: '../index/index',
                })
              }
            });
          };

        }
      }),
      //定位 获取用户定位
      wx.getLocation({
        type: 'gcj02', //返回可以用于wx.openLocation的经纬度
        success: function (res) {
          that.setData({
            latitudeCur: res.latitude,
            longitudeCur: res.longitude
          });
          that.checkFlag();
        },
        // fail() {

        //   wx.showModal({
        //     title: '定位失败',
        //     content: '请打开手机GPS或其他定位开关。',
        //     success: function (res) {
              // 用户没有授权成功，不需要改变 isHide 的值
              // if (res.confirm) {
              //   console.log('用户点击了“重新定位”');
              //   wx.getLocation({
              //     type: 'gcj02', //返回可以用于wx.openLocation的经纬度
              //     success: function (res) {
              //       that.setData({
              //         latitudeCur: res.latitude,
              //         longitudeCur: res.longitude
              //       });
              //       that.checkFlag();
              //     },
              //   });
              // }
        //     }
        //   })
        // }
      })
  },

  checkFlag: function () {
    if (this.data.wxUserInfo) {
      // if (this.data.wxUserInfo && this.data.latitudeCur && this.data.longitudeCur) {
      if (this.data.typedata == "紧急") {
        this.sendReq("全部", "true");
      } else {
        this.sendReq(this.data.typedata, "false");
      }
    }
  },

  onShow: function () {
    wx.getSetting({
      success(res) {
        //如果定位 未授权拉起授权
        if (!res.authSetting['scope.userLocation']) {
          wx.authorize({
            scope: 'scope.userLocation',
            success() {
              that.openConfirm(); //如果拒绝，在这里进行再次获取授权的操作
              console.log("用户已经同意位置授权");
            },
            fail() {
              console.log("用户已经拒绝位置授权");
              that.openConfirm(); //如果拒绝，在这里进行再次获取授权的操作
            }
          })
        }
      }
    });



    //获取用户信息
    var that = this;
    app.getUserInfo(function (userInfo) {
      that.setData({
        wxUserInfo: userInfo
      });
      that.checkFlag();
    });
    //定位
    wx.getLocation({
      type: 'gcj02', //返回可以用于wx.openLocation的经纬度
      success: function (res) {
        that.setData({
          latitudeCur: res.latitude,
          longitudeCur: res.longitude
        });
        that.checkFlag();
      },
      fail() {
        wx.showModal({
          title: '定位失败',
          content: '请打开手机GPS或其他定位开关。',
          success: function (res) {
            // 用户没有授权成功，不需要改变 isHide 的值
            if (res.confirm) {
              console.log('用户点击了“重新定位”');
              wx.getLocation({
                type: 'gcj02', //返回可以用于wx.openLocation的经纬度
                success: function (res) {
                  that.setData({
                    latitudeCur: res.latitude,
                    longitudeCur: res.longitude
                  });
                  that.checkFlag();
                },
              });
            }
          }
        })
      }
    })
  },
})