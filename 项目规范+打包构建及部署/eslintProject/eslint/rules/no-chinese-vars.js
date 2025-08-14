// 规则的本质是一个对象，
// 插件化体系中，这个对象的属性约束就是我们讲的插件化协议
export const noChineseVars = {
  // 插件的元信息
  meta:{
    messages:{
      noChineseName:'不允许使用中文' // noChineseName对应Identifier中的messageId
    }
  },
  // 插件的入口,插件上下文
  create (context) {
    return {
      // 访问者模式，访问到某一个ast节点时就进行处理
      VariableDeclaration(node){
        console.log('VariableDeclaration',node);
      },
      VariableDeclarator(node){
        console.log(node);
      },
      Identifier(node){
        console.log(node);
        if (node.name == 'chinese') {
          context.report({
            node,
            messageId:'noChineseName'
          })
        }
      },
      Literal(node){
        console.log(node);
      },
    }
  }
}
