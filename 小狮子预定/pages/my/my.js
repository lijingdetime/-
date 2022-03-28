// pages/my/my.js
//var VcollegeItems = require('Vdata.js')
Page({
  data: {
    index: 0,
  },
  addressChoiceTap: function () {
    var that = this
    wx.chooseAddress({
      success: function (res) {
        that.setData({
          userName: res.userName,
          provinceName: res.provinceName,
          cityName: res.cityName,
          countyName: res.countyName,
          detailInfo: res.detailInfo,
          telNumber: res.telNumber
        })
      }
    })
  },
  collegeChoiceTap: function (e) {
    if (this.data.index !== e.detail.value) {
      getApp().globalData.college_change = true
      this.setData({
        index: e.detail.value
      })
    }
  },
  getZones: function () {
    var that = this
    wx.request({
      url: getApp().globalData.base_url + 'zones', //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + that.data.token
      },
      success: function (res) {
        let items_list = []
        for (let zone of res.data) {
          items_list.push(zone.name)
        }
        that.setData({
          collegeItems: items_list
        })
      }
    })
  },
  updateAddressInfo: function () {
    try {
      const value = this.data.token;
      if (value) {
        // Do something with return value
        wx.request({
          url: getApp().globalData.base_url + 'account-user-RetrieveUpdate', //仅为示例，并非真实的接口地址
          method: 'PUT',
          header: {
            'content-type': 'application/json', // 默认值
            'Authorization': 'Token ' + value
          },
          data: {
            name: this.data.userName,
            province: this.data.provinceName,
            city: this.data.cityName,
            county: this.data.countyName,
            detail: this.data.detailInfo,
            mobile: this.data.telNumber,
            zone: this.data.collegeItems[this.data.index],
            the_index: this.data.index
          },
          success: function (res) {
            if (res.statusCode == '200') {
              console.log()
            }
            else {
              console.log('error 1 :update返回值但是报错', res)
              console.log('the res.data:', res.data)
            }
          }
        })
      }
    } catch (e) {
      // Do something when catch error
      console.log('error 2 :没有update成功')
      this.createAddressInfo()
    }
  },
  createAddressInfo: function () {
    try {
      const value = this.data.token;
      if (value) {
        // Do something with return value
        wx.request({
          url: getApp().globalData.base_url + 'account-user-Create', //仅为示例，并非真实的接口地址
          method: 'POST',
          header: {
            'content-type': 'application/json', // 默认值
            'Authorization': 'Token ' + value
          },
          data: {
            name: this.data.userName,
            province: this.data.provinceName,
            city: this.data.cityName,
            county: this.data.countyName,
            detail: this.data.detailInfo,
            mobile: this.data.telNumber,
            zone: this.data.collegeItems[this.data.index],
            the_index: this.data.index
          },
          success: function (res) {
            if (res.statusCode == '201') {
              console.log()
            }
            else {
              console.log('error 3 :返回值但是报错,很可能是由于已经创建过了', res)
            }
          }
        })
      }
    } catch (e) {
      // Do something when catch error
      console.log('error 4 :没有create成功')
    }
  },
  getAddressInfo: function () {
    var that = this
    try {
      const value = that.data.token;
      if (value) {
        // Do something with return value
        wx.request({
          url: getApp().globalData.base_url + 'account-user-RetrieveUpdate', //仅为示例，并非真实的接口地址
          method: 'GET',
          header: {
            'content-type': 'application/json', // 默认值
            'Authorization': 'Token ' + value
          },
          success: function (res) {
            //console.log(typeof res.statusCode);
            if (String(res.statusCode) == '200') {
              that.setData({
                userName: res.data.name,
                telNumber: res.data.mobile,
                provinceName: res.data.province,
                cityName: res.data.city,
                detailInfo: res.data.detail,
                countyName: res.data.country,
                index: res.data.the_index
              })
            }
            else {
              that.setData({
                addressData: null,
              })
            }
          }
        })
      }
    } catch (e) {
      // Do something when catch error
      console.log('error 5 :没有request成功', e)
    }
  },
  get_productInformation: function () {
    var token = wx.getStorageSync('token')
    var that = this
    //获取pd
    wx.request({
      url: getApp().globalData.base_url + + 'product-abstract', //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + token
      },
      success: function (res) {
        //这里需要数据处理，按类别分类出banner
        let product_one = []
        let product_two = []
        let product_three = []
        let product_four = []
        for (let product of res.data) {
          if (product.productType == '商品类型1') {
            product_one.push(product)
          }
          else if (product.productType == '商品类型2') {
            product_two.push(product)
          }
          else if (product.productType == '商品类型3') {
            product_three.push(product)
          }
          else if (product.productType == '商品类型4') {
            product_four.push(product)
          }

        }
        that.setData({
          product_one: product_one,
          product_two: product_two,
          product_three: product_three,
          product_four: product_four,
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var value = wx.getStorageSync('token')
    //var value = "5baac3e67c5a97f0c5b72c9c175ea0b6422358b9"
    this.setData({
      token: value
    })
    this.getAddressInfo()
    this.getZones()
    // this.setData({
    //   collegeItems: this.data.zones
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
    this.updateAddressInfo()
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