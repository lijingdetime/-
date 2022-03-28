// pages/up_images/up_images.js
Page({
  data: {
    selectedImage: []
  },
  upper: function (e) {
    console.log(e)
  },
  lower: function (e) {
    console.log(e)
  },
  scroll: function (e) {
    console.log(e)
  },
  tapUp: function (e) {
    var that = this
    wx.chooseImage({
      count: 20,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        console.log('##########################################')
        console.log(res.tempFilePaths)
        console.log('##########################################')
        that.setData({
          selectedImage: res.tempFilePaths
        })
      }
    })
  },
  tapRemove: function (e) {
    let aim_array = this.data.selectedImage
    aim_array.splice(-1, 1)
    this.setData({
      selectedImage: aim_array
    })
  },
  reallyUpImages_one: function (e) {
    wx.uploadFile({
      url: 'http://127.0.0.1:8000/order-images/', //仅为示例，非真实的接口地址
      filePath: this.data.selectedImage[0],
      method: 'POST',
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + wx.getStorageSync('token')
      },
      name: 'file',
      formData: {
        'user': 'a test man'
      },
      success: function (res) {
        console.log(res.data)
      }
    })
  },
  reallyUpImages_two: function (e) {
    wx.request({
      url: 'http://127.0.0.1:8000/order-images/', //仅为示例，并非真实的接口地址
      data: {
        'image':this.data.selectedImage[0]
        },
      method: 'POST',
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token ' + wx.getStorageSync('token')
      },
      success: function (res) {
        console.log(res.data)
      }
    })
  }
})
