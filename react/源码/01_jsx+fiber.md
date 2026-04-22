
# 一：虚拟DOM与jsx转换
  ### 1.虚拟DOM的what,why,where,how
   - where:react中的哪里用到了虚拟DOM?**渲染时**react根据jsx函数生成了**VDOM**（ReactElement）,状态变化的时候：生成新的VDOM,Diff算法对比新旧VDOM
  ### 2.实现jsx方法
  - jsxDEV(dev环境)
  - jsx方法(prod环境)
  - React.createElement方法
    ```js
      const ReactElement = function (type: Type, key: Key, ref: Ref, props: Props): ReactElement {
        const element = {
          $$typeof: REACT_ELEMENT_TYPE,
          type,
          key,
          ref,
          props,
          __mark: 'hahatuzi'
        }
        return element
      }

      export const jsx = (type:ElementType, config:any, ...children:any) => {
        let key:Key = null;
        const props:Props = {};
        let ref:Ref = null;
        for (const prop in config) {
          const val = config[prop]
          if(prop == 'key'){
            if (val != undefined){
              key = '' + val
            }
            continue
          }
          if(prop == 'ref'){
            if (val != undefined){
              ref = '' + val
            }
            continue
          }
          if({}.hasOwnProperty.call(config, prop)){
            props[prop] = val
          }
        }
        const childrenlength = children.length
        if(childrenlength){
          if (childrenlength == 1) {
            props.children = children[0];
          } else {
            props.children = children;
          }
        }
        return ReactElement(type, key, ref, props)
      }

      export const jsxDEV = jsx;
    ```

  ### 3.实现打包流程：针对上述3个方法打包对应文件
  - react/jsx-dev-runtime.js(dev环境)
  - react/jsx-runtime.js(prod环境)
  - react
  ### 4.实现调试打包结果的环境
  ### 5.jsx的本质是什么
  ### 6.reactELement和FiberNode的关系




# 三：Fiber协调流程
  ### 协调阶段（可中断）：
增量构建 Fiber 树，标记副作用（effectTag）。
通过 requestIdleCallback 或 Scheduler 包分片执行。
  ### 提交阶段（同步不可中断）：
遍历副作用链表，执行 DOM 操作和生命周期方法。
# 二：reconciler
  ### 3.reconciler的工作方式
  对于同一个节点，比较其ReactElement与fiberNode,生成子fiberNode,根据比较结果生成各种标记（插入，删除，移动。。）
  ```js
  // 举例：挂载div
  // jsx('div') ---> (和对应的fiberNode) null --->  生成fiberNode --> 对应的标记 Placement
  // 将div更新为P
  // jsx(p) ---> fiberNode type:'div' --> 生成子fiberNode --> 对应标记 Deletion Placement
  ```
  ### 4.双缓冲技术
  当所有ReactElement比较完毕后，会生成一颗fiberNode树，项目一共存在两棵fiberNode树：current，workProgress。
  - current：对应真实UI的fiberNode树。
  - workProgress:触发更新后，正在reconclier中计算的fiberNode树
# jsx消费的顺序:DFS深度优先遍历的顺序遍历ReactElement，所以组件销毁的时候子组件优先被销毁


