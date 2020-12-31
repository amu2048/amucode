var INTERFACES = require('../../util/interfaceUrls.js');

var app = getApp();
Page({
    data:{
        wechatUserInfo:{},
        scrollHeight:100, //文本框的滑动块高度
        imageWidth:125, //上传的图片高宽
        imageHeight:125,
        photoList:[],
        location:"选择您的位置",
        array: ['取餐','取快递', '带文件', '租房','美食推荐', '其他'],
        index: 0,
        date:"2021-01-01",
        time:"13:14",
        curtype: "请选择"
    },
    addAndSavePhoto:function(){
        console.log("从本地选取照片");
        var that = this;
        var showFileList = that.data.photoList;
        wx.chooseImage({
          count: 9, // 最多可以选择的图片张数，默认9
          sizeType: ['original','compressed'], // original 原图，compressed 压缩图，默认二者都有
          sourceType: ['album', 'camera'], // album 从相册选图，camera 使用相机，默认二者都有
          success: function(res){
            // 后台慢慢保存文件到本地      
            res.tempFilePaths.forEach(function(tempFilePath){
                // 调用保存到本地的API
                wx.saveFile({
                  tempFilePath: tempFilePath,
                  success: function(res){
                    console.log("保存到本地的文件路径："+res.savedFilePath);
                    showFileList.push(res.savedFilePath);
                    // 更新页面显示
                    console.log(showFileList.length+"个展示图片");
                    that.setData({
                        photoList:showFileList
                    });
                  }
                })
            }); 
          }
        });
    },
    previewPhoto:function(event){
        console.log(event);
        var curTarget = event.target.dataset.imageSrc;
        console.log(curTarget);
        wx.navigateTo({
          url: '../previewphoto/previewphoto?imagepath='+curTarget
        });
    },
    twoColomn:function(){
        var that = this;
        var length = 750/2;
        that.setData({
            imageWidth:length,
            imageHeight:length
        });
    },
    threeColomn:function(){
        var that = this;
        var length = 750/3;
        that.setData({
            imageWidth:length,
            imageHeight:length
        });
    },
    fourColomn:function(){
        var that = this;
        var length = 750/4;
        that.setData({
            imageWidth:length,
            imageHeight:length
        });
    },
    //选择求助类型重写 选定的类别值
    bindPickerChange: function(e) {
        console.log('picker改变求助类型，值', e.detail.value)
        var that = this;
        var i=e.detail.value; 
        that.setData({
        index: i,
        curtype:that.data.array[i]
        });
        console.log("123")
    },
    //选择任务的有效期 出发函数 重写希纳是的有效期
    bindDateChange:function(e){
        this.setData({
            date:e.detail.value
        })
    },
    //选择地图出发的函数 重写选择的地图位置
    chooseLocation:function(){
        var that = this;
        wx.chooseLocation({
            type: 'wgs84',
            success: function(res) {
                var latitudeCur = res.latitude;
                var longitudeCur = res.longitude;
                var name = res.name;
                var address = res.address;
                console.log("地点名字",name,"地址",address);
                that.setData({
                    location:name,//选择的地址
                    latitude:latitudeCur,//选择的经度
                    longitude:longitudeCur//选择的纬度
                })
            }
        });
    },

    onLoad:function(){
        console.log("加载照片列表");
        var that = this;
        //获取用户信息
        app.getUserInfo(function(userInfo){
            //更新数据
            that.setData({
                wechatUserInfo:userInfo
            })
            that.update()
        })
        // 获取当前窗口高度，以便设置scrollView的高度
        wx.getSystemInfo({
          success: function(res) {
            console.log(res.model);
            console.log(res.pixelRatio);
            console.log(res.windowWidth);
            console.log(res.windowHeight);
            console.log(res.version);
            that.setData({
                scrollHeight:res.windowHeight/8
            });
          }
        });
        //获取当前时间
        var timeStr =new Date;
        function formatNumber(n) {
            n = n.toString()
            return n[1] ? n : '0' + n
            }

        function formatTime(time) {
            var hour = time.getHours()
            var minute = time.getMinutes()
            var second = time.getSeconds()
           
            return [hour, minute].map(formatNumber).join(':')
            }

        function formatDate(date) {
            var year = date.getFullYear()
            var month = date.getMonth() + 1
            var day = date.getDate()

            return [year, month, day].map(formatNumber).join('-')
            }

        var dateNow=formatDate(timeStr);
        // var timeNow=formatTime(timeStr);
        that.setData({
                date:dateNow,
                // time:timeNow
            });
    },
    //发布求助 出发函数
    formSubmit: function(e) {
        var that = this;
        console.log('form发生了submit事件，携带数据为：', e.detail.value)
        var formData=e.detail.value;//提交表单form获取的数据
        var reqData={};//请求数据
        reqData.userId=that.data.wechatUserInfo.nickName;//微信登录的名字
        reqData.userUrl=that.data.wechatUserInfo.avatarUrl;//微信登录的头像地址
     
        reqData.longitude=that.data.longitude;//经度
        reqData.latitude=that.data.latitude;//纬度
        reqData.srvType=that.data.curtype;//求助类型，在选择求助类型时 已经触发重写 所以这里再data数据中获取
        reqData.srvTitle=formData.title;//求助标题
        reqData.srvDesc=formData.describe;//求助内容
        reqData.srvCost=formData.score;//悬赏积分
        reqData.endTime=formData.date+" 00:00:00";//求助有效期
        reqData.urgent=formData.isquickly;//是否是加急
        reqData.mobile=formData.phonenumber;//求助人的电话号
        reqData.posDes=that.data.location;//求助的地址
        if(reqData.longitude ==null){
            wx.showModal({
                title: '提示',
                content: '请选择您的位置',
                success: function(res) {
                    if (res.confirm) {
                        console.log('用户点击确定')
                    }
                }
            });
        }
        else{
        wx.request({
            url: INTERFACES.postNeed,//调用INTERFACES中的添加需求接口
            data: reqData,
            method:"POST",
            header: {
               //'content-type': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                "dataType":"json"
            },
            success: function(res) {
                if (res.data.respCode){
                    if(res.data.respCode==0){
                        wx.showModal({
                            title: '提示',
                            content: '求助信息提交成功！',
                            success: function(res) {
                                if (res.confirm) {
                                    console.log('用户点击确定')
                                    wx.navigateBack({
                                        delta: 2
                                      });
                                    } else if (res.cancel) {
                                    console.log('用户点击取消')
                                    }
                            }
                        });
                    }
                    else if(res.data.respCode==101){
                        wx.showModal({
                            title: '提示',
                            content: '积分不足！修改积分重新发布！',
                            success: function(res) {
                                if (res.confirm) {
                                    console.log('用户点击确定')
                                }
                            }
                        });
                    }
                    else if(res.data.respCode==1){
                        wx.showModal({
                            title: '提示',
                            content: '求助信息提交失败!',
                            success: function(res) {
                                if (res.confirm) {
                                    console.log('用户点击确定')
                                }
                            }
                        });
                    }
                }
                else{
                    wx.showModal({
                        title: '提示',
                        content: '求助信息提交失败!',
                        success: function(res) {
                            if (res.confirm) {
                                console.log('用户点击确定')
                            }
                        }
                    });
                }
            },
            fail: function() {
                wx.showModal({
                    title: '提示',
                    content: '提交失败!',
                    success: function(res) {
                        if (res.confirm) {
                            console.log('用户点击确定')
                        }
                    }
                });
            }
        });
    }},
    onShow:function(){
        console.log("显示图片")
        // 获取本地保存的图片
        var that = this;
        wx.getSavedFileList({
          success: function(res){
            // success
            console.log(res.errMsg);
            console.log(res.fileList.length+"个本地文件");
            var filePathList=[];
            res.fileList.forEach(function(item){
                filePathList.push(item.filePath);
                // 删除本地文件
               wx.removeSavedFile({
                  filePath: item.filePath,
                  complete: function(res){
                    // success
                    console.log(res);
                  }
                })   
            });
            that.setData({
                photoList:filePathList
            });
          },
          fail:function(){
              // 失败 wx.showToast
              wx.showToast({
                  title:"获取本地图片失败！",
                  duration: 2000
              });
          }
        })
    }
})