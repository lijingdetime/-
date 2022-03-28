// pages/home/home.js

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  productTap: function (event) {
    const productId = event.currentTarget.dataset.productid;
    const bartitle = event.currentTarget.dataset.bartitle;
    wx.navigateTo({
      url: '../detail/detail?id=' + productId + "&bartitle=" + bartitle,
    })
  },
  get_productInformation: function (options){
    try{
      var value = wx.getStorageSync('token')
      var that = this
      //获取pd
      wx.request({
        url: 'http://127.0.0.1:8000/' + 'product-abstract', //仅为示例，并非真实的接口地址
        header: {
          'content-type': 'application/json', // 默认值
          'Authorization': 'Token ' + value
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

    }catch(e){
      console.log('没有product数据')
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.get_productInformation()
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
    // if (getApp().globalData.college_change) {
    //   this.get_productInformation()
    //   getApp().globalData.college_change = false
    //   console.log(getApp().globalData.college_change)
    // } 
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
    console.log('页面卸载')
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    if (getApp().globalData.college_change) {
      this.get_productInformation()
      getApp().globalData.college_change = false
      console.log(getApp().globalData.college_change)
    } 
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
//导出要用的函数
