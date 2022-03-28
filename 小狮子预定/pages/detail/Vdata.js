const productDetail=[
  {order:1,id:1,textType: 'true', name:'id1',placeholder:'请留下一句话',radioItem:'',checkItems:'',array:''},
  { order: 2,id:2, textareaType: 'true', name: 'id2', placeholder: '请留下二句话', radioItem: '', checkItems: '', array: '' },
  { order: 3, id: 3, name: 'id3', textType: '', pickerType: 'true', placeholder: 'id3 placeholder', radioItem: '', checkItems: '', pickerItems: ["ba", "la", 'ma'], prompt:'选择一个嘛'},
  { order: 4,id: 4, prompt:'radio选择国家',radioType: 'true', name: 'id4', placeholder: 'id4 placeholder', radioItems: [{ name: '美国', value: '美国' },{ name: '中国', value: '中国', checked: 'true' },{ name: 'BRA', value: '巴西' },{ name: 'JPN', value: '日本' },{ name: 'ENG', value: '英国' },{ name: 'TUR', value: '法国' }], checkItems: '', array: '' },
  {
    order: 5,
    id: 5, prompt:'checkbox复选框',checkboxType: 'true', name: 'id5', checkboxItems: [{ name: '美国', value: '美国' },
    { name: '中国', value: '中国', checked: 'true' },
    { name: 'BRA', value: '巴西' },
    { name: 'JPN', value: '日本' },
    { name: 'ENG', value: '英国' },
    { name: 'TUR', value: '法国' }
]}
]

const trueapi=[
  {
    id:3,
    selectType:'checkbox',
    order:"3",
    placeholder:'暖暖的太阳',
    prompt: "[{ '美国','美国' },{ '中国', '中国', 'true' },{ 'BRA', '巴西' },{ 'JPN', '日本' },{'ENG',  '英国' },{ 'TUR','法国' }]",
    product:2,
  },
  {
    id: 2,
    selectType: 'radio',
    order: "1",
    placeholder: '冷冷的冰雨',
    prompt: "[{ '美国', '美国' },{ '中国', '中国', 'true' },{ BRA', '巴西' },{'JPN', '日本' },{  'ENG','英国' },{ 'TUR', '法国' }]",
    product: 2,
  },
  {
    id: 1,
    selectType: 'picker',
    order: "2",
    placeholder: '选择一个嘛',
    prompt: '[ba, la, ma]',
    product: 2,
  },
  {
    id: 5,
    selectType: 'text',
    order: "4",
    placeholder: '这个是text',
    prompt: '',
    product: 2,
  },
  {
    id: 4,
    selectType: 'textarea',
    order: "5",
    placeholder: '这是textarea',
    prompt: '',
    product: 2,
  }
]

module.exports = {
  productDetail: productDetail,
  trueapi: trueapi
}

// radioItems: [
//   { name: '美国', value: '美国' },
//   { name: '中国', value: '中国', checked: 'true' },
//   { name: 'BRA', value: '巴西' },
//   { name: 'JPN', value: '日本' },
//   { name: 'ENG', value: '英国' },
//   { name: 'TUR', value: '法国' },
// ],
//   checkboxItems: [
//     { name: '美国', value: '美国' },
//     { name: '中国', value: '中国', checked: 'true' },
//     { name: 'BRA', value: '巴西' },
//     { name: 'JPN', value: '日本' },
//     { name: 'ENG', value: '英国' },
//     { name: 'TUR', value: '法国' },
//   ],
//     array: ['美国', '中国', '巴西', '日本'],
//       index: 0,