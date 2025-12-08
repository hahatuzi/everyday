# excel相关插件
  - 内容解析插件：xlsx
  - 预览插件：vue(@vue-office/excel),react(react-file-viewer)
# xlsx产物转化示意图：
  Blob文件流 --> arrayBuffer --> Read方法读取为book对象（book对象为整个excel文件） -->  提取为对应的sheet对象（sheet对象为excel文件中的单个sheet工作簿） --> 创建workbook --> 输出为excel文件