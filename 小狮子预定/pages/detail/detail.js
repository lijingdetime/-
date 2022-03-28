// pages/detail/detail.js
var VproductDetail = require('Vdata.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {
    NavigationBarTitle: null,
    pd: []
  },
  radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value)
  },
  checkboxChange: function (e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      thisIndex: e.detail.value
    })
  },
  up_data: function (up_data) {
    var token = wx.getStorageSync('token')
    wx.request({
      url: getApp().globalData.base_url + 'order/' + this.data.productID, //仅为示例，并非真实的接口地址
      data: up_data,
      method: 'POST',
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + token
      },
      success: function (res) {
        console.log('数据上传成功，返回结果为:')
        console.log(res.data)
      }
    })
  },
  formSubmit: function (e) {
    //把需要上传数据中的数组转化为字符串
    const objkeys = Object.keys(e.detail.value);
    const obj_length = objkeys.length;
    for (let argument of objkeys) {
      if (typeof e.detail.value[argument] == 'object') {
        let docker = ''
        for (let item of e.detail.value[argument]) {
          docker = docker + item.toString();
        }
        e.detail.value[argument] = docker;
      }
    }
    //上传数据
    this.up_data(e.detail.value);
    wx.showToast({
      title: '成功',
      icon: 'success',
      duration: 2000
    })
  },
  formReset: function () {
    this.setData({
      thisIndex: null,
    })
  },
  get_data: function () {
    let pd_data = this.data.pd;
    for (let detail of pd_data) {
      if (detail.selectType == 'show-picture') {
        let sp = detail.image.image_select.split('/')
        detail.image.image_select = getApp().globalData.base_url + 'static/images/' + sp[7] + '/' + sp[8] + '/' + sp[9] + '/' + sp[10];
        detail.showPicture_selected = 'True';
      }
      if (detail.prompt == null) {
        if (detail.selectType == 'text') {
          detail.text_selected = 'True';
          console.log('text');
        }
      }
      else {
        var regs = new RegExp("'", "gi");
        let re_data = detail.prompt.replace('[(', '').replace(')]', '').replace('[', '').replace(']', '').replace(regs, '')
        if (detail.selectType == 'picker') {
          detail.prompt = re_data.split(',');
          detail.picker_selected = 'True';
        }
        else if (detail.selectType == 'text') {
          detail.text_selected = 'True';
        }
        else if (detail.selectType == 'textarea') {
          detail.textarea_selected = 'True';
        }
        else if (detail.selectType == 'show-title') {
          detail.showTitle_selected = 'True';
        }
        else if (detail.selectType == 'show-text') {
          detail.showText_selected = 'True';
        }
        else {
          if (detail.selectType == 'radio') {
            detail.radio_selected = 'True';
          }
          else if (detail.selectType == 'checkbox') {
            detail.checkbox_selected = 'True';
          }
          let process_data = re_data.split('), (');
          for (var i = 0; i < process_data.length; i++) {
            process_data[i] = process_data[i].split(',');
            if (process_data[i].length == 3) {
              process_data[i] = {
                name: process_data[i][0],
                value: process_data[i][1],
                checked: process_data[i][2],
              }
            } else {
              process_data[i] = {
                name: process_data[i][0],
                value: process_data[i][1],
              }
            }
          };
          detail.prompt = process_data;
        }


      }
      detail.order = parseInt(detail.order)
    }
    pd_data = pd_data.sort(function (a, b) {
      return a.order - b.order;
    }),
      this.setData({
        productDetail: pd_data
      })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      NavigationBarTitle: options.bartitle,
      productID: options.id
    })
    //改变从这里开始，感觉应该用fetch
    var that = this
    //获取pd
    wx.request({
      url: getApp().globalData.base_url + 'product/' + options.id + '/detail', //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + wx.getStorageSync('token')
      },
      success: function (res) {
        that.setData({
          pd: res.data
        })
        that.get_data();
      }
    })
    wx.request({
      url: getApp().globalData.base_url + 'advertisingInfoList/' + options.id, //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + wx.getStorageSync('token')
      },
      success: function (res) {
        for (let d of res.data) {
          let st = d.banner_images.replace('/advertisingInfoList', '');
          d.banner_images = st
        }
        that.setData({
          advertisingInfo: res.data
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    if (this.data.NavigationBarTitle) {
      wx.setNavigationBarTitle({
        title: this.data.NavigationBarTitle,
      })
    } else {
      wx.setNavigationBarTitle({
        title: "小狮子预定",
      })
    }
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
    console.log('下拉')
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