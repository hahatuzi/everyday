export default{
  rules:{
    "no-unused-vars":"error", // 不允许声明没有使用的变量
    "no-console":"error",// 不允许打印console
    "no-sparse-arrays":"error", // 不允许组数定义的时候有多余的逗号
    "no-undef":"error", // 不允许未声明的变量
    "no-unreachable":"error", // 不允许函数return后还写代码
    "no-dupe-keys":"error", // 不允许对象有重复的key
  }
}