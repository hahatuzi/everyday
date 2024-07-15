export {}
function updateData () {
  const arr:Data[] = getList()
  const last:Data = arr[arr.length - 1]
  // 每次刷新时，数组都新增一条刷新纪录
  let obj:Data = {
    count:last ? last.count + 1 : 1,
    time:new Date().toLocaleTimeString()
  }
  arr.push(obj)
  console.log(obj)
  // 获取刷新列表
  console.log(render(arr))
  setList(arr)
}
const KEY = 'dataKey'
type Data = {
  count:number,
  time:string
}
function getList () {
  const list:Data[] = JSON.parse(localStorage.getItem(KEY) || '[]')
  return list
}
function render (list:Data[]) {
  let str:string =  list.map(item => {
    return '刷新次数为：' + item.count + ',' + '当前刷新时间为：' + item.time
  }).join('<br/>')
  return str
}
function setList(list:Data[]) {
  localStorage.setItem('KEY',JSON.stringify(list))
}
updateData()