// 先声明
function add (arg1:string, arg2:string):string
function add (arg1:string, arg2:string):number

// 实现
function add (arg1:string | number, arg2:string | number){
  if (typeof arg1 == 'string' && typeof arg2 == 'string') {
    return arg1 + arg2
  } else if (typeof arg1 == 'number' && typeof arg2 == 'number') {
    return arg1 + arg2
  }
}