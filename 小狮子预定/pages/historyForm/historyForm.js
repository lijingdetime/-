// pages/historyForm/historyForm.js
var util = require('../../utils/util.js')
Page({
  data: {
    dateTime: [],
    subInfo: ['submit1', 'submit2', 'submit3', 'submit4', 'submit5', 'submit6', 'submit7', 'submit8', 'submit9', 'submit10', 'submit11', 'submit12', 'submit13', 'submit14', 'submit15', 'submit16', 'submit17', 'submit18', 'submit19', 'submit20']
  },
  onLoad: function () {
    this.setData({
      dateTime: util.formatTime(new Date())
    })
    this.get_orderInformation()
  },
  get_orderInformation: function (options) {
    try {
      var value = wx.getStorageSync('token')
      var that = this
      //获取pd
      wx.request({
        url: getApp().globalData.base_url + 'order-list', //仅为示例，并非真实的接口地址
        header: {
          'content-type': 'application/json', // 默认值
          'Authorization': 'Token ' + value
        },
        success: function (res) {
          //这里需要数据处理，按类别分类出banner
          let aim_fields=that.data.subInfo
          for(let order of res.data){
            order.create_time=order.create_time.substring(0,16);
            let aim_string = ''
            for(let i of aim_fields){
              if(order[i]==''){
                continue;
              }
              else{
                aim_string = aim_string + '>'+order[i];
              }
            }
            order.sumInfo=aim_string;
          }
          that.setData({
            orderInformation:res.data
          })
        }
      })

    } catch (e) {
      console.log('没有order数据')
    }
  },
  onPullDownRefresh: function () {
    this.get_orderInformation()
  },
})