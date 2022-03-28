//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: '欢迎来到小狮子预定',
    userInfo: {}
  },
  //事件处理函数
  bindViewTap: function () {
    wx.switchTab({
      // url: '../logs/logs'
      url: '../home/home'
    })
  },
  checkAndLogin: function () {
    wx.checkSession({
      success: function () {
        //session 未过期，并且在本生命周期一直有效
        console.log('session 未过期，并且在本生命周期一直有效')
      },
      fail: function () {
        //登录态过期
        wx.login({
          success: function (res) {
            if (res.code) {
              //发起网络请求
              wx.request({
                url: 'http://127.0.0.1:8000/token',
                method: 'POST',
                header: {
                  'content-type': 'application/json'
                },
                data: {
                  code: res.code
                },
                success: function (res) {
                  try {
                    wx.setStorageSync('token', res.data)
                  } catch (e) {
                    console.log(e)
                  }
                }
              })
            } else {
              console.log('获取用户登录态失败！' + res.errMsg)
            }
          }
        });
      }
    })
  },
  upLoadData: function (data) {
    wx.request({
      url: 'test.php', //仅为示例，并非真实的接口地址
      data: data,
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(res)
      },
      fail: function (res) {
        console.log('up data:', data)
      }
    })
  },
  onLoad: function () {
    console.log('onLoad')
    this.checkAndLogin()
    var that = this
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function (userInfo) {
      //更新数据
      that.setData({
        userInfo: userInfo
      })
    })
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          systemInfo: res
        })
      }
    });
    wx.getNetworkType({
      success: function (res) {
        that.setData({
          networkType: res.networkType
        })
      }
    })
  },
  onUnload:function(){
    let updata = {
      userInfo: this.data.userInfo,
      systemInfo: this.data.systemInfo,
      networkType: this.data.networkType
    }
    this.upLoadData(updata)
  }
})
