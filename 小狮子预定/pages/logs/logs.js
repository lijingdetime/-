//logs.js
var VproductDetail = require('../detail/Vdata.js')
var util = require('../../utils/util.js')
Page({
  data: {
    logs: [],
    pd:[]
  },
  onLoad: function () {
    var that=this
    that.setData({
      logs: (wx.getStorageSync('logs') || []).map(function (log) {
        return util.formatTime(new Date(log))
      })
    })
    // this.get_my_data('product/2/detail')
    wx.request({
      url: 'http://127.0.0.1:8000/' + 'product/2/detail', //仅为示例，并非真实的接口地址
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': 'Token b2f2806a0ff8b8ea50da908c646b62cedacd65eb'
      },
      success: function (res) {
        that.setData({
          pd:res.data
        })
      }
    })
    //console.log(this.data.mydata)
    //从服务器请求数据
    //使用util.request_my_data函数但是函数有问题，没能返回值
    // util.request_my_data('product/2/detail', '', callBack)
    // function callBack(res) {
    //   that.setData({
    //     my_data: res,
    //   })
    // }
    //console.log(this.data.my_data)
  },
  onPullDownRefresh: function () {
    let pd_data = this.data.pd;
    for (let detail of pd_data) {
      let re_data = detail.prompt.replace('[(', '').replace(')]', '').replace('[', '').replace(']', '')
      if(detail.selectType=='picker'){
        detail.prompt = re_data.split(',');
        detail.picker_selected='True';
      }
      else if (detail.selectType == 'text'){
        detail.text_selected = 'True';
      }
      else if (detail.selectType == 'textarea'){
        detail.textarea_selected = 'True';
      }
      else{
        if (detail.selectType == 'radio'){
          detail.radio_selected = 'True';
        }
        else if (detail.selectType == 'checkbox'){
          detail.checkbox_selected = 'True';
        }
        let process_data = re_data.split('), (');
        for(var i=0;i<process_data.length;i++){
          process_data[i]=process_data[i].split(',');
          if(process_data[i].length==3){
            process_data[i] = {
              name: process_data[i][0],
              value: process_data[i][1],
              checked: process_data[i][2],
            }
          }else{
            process_data[i] = {
              name: process_data[i][0],
              value: process_data[i][1],
            }
          }        
        };
        detail.prompt = process_data;
      }
      detail.order=parseInt(detail.order)
    }
    pd_data=pd_data.sort(function(a,b){
      return a.order-b.order;
    })
    console.log(pd_data);
  }
})
// 要点
// 1 parseInt
// 2 sort
// 3 
// process_data[i] = {
//   name: process_data[i][0],
//   value: process_data[i][1],
// }
// 困局：为甚像是被阻止在了第二层if...else if..,进不了第三个else