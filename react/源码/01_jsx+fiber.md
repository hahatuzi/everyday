
# 一：VDOM与jsx转换
  ### 1.虚拟DOM的，what,why,where,how
   - where:react中的哪里用到了虚拟DOM?**渲染时**react根据jsx函数生成了**VDOM**（ReactElement）,状态变化的时候：生成新的VDOM,Diff算法对比新旧VDOM
  ### 1.实现jsx方法
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
  ### 2.实现打包流程：针对上述3个方法打包对应文件
  - react/jsx-dev-runtime.js(dev环境)
  - react/jsx-runtime.js(prod环境)
  - react
  ### 3.实现调试打包结果的环境

# 二：Fiber
  - fiberNode是虚拟DOM在react中的实现方式。vue中叫VNode。
  - 它介于React Element和真实UI节点之间，能够表达节点之间的关系，转换过程为JSX --> ReactElement --> FIberNode--> DomElement。
  ### 1.ReactElement
  ReactElement如果作为核心模块操作的数据结构，存在以下问题：
   - 无法表达节点之间的关系
   - 字段有限，不好扩展
  所以需要一种新的数据结构，也就是FiberNode。

  ### 2.Fiber的特点
   - (1)**实现增量式渲染**：将渲染工作拆分成多个块，并分散在多个帧上进行处理
   - (2)**可中断任务**：支持暂停，中止，或者复用工作单元work
   - (3)**优先级调度**：给不同类型的work赋予优先级，比如用户输入可以打断数据更新任务
   - (4)**并发模式基础**：为Suspense,useTransition等特性提供底层支持

  ### 3.Fiber分类
  项目一共存在两棵fiberNode树：current，workProgress。
   - (1)current：对应真实UI的fiberNode树。
   - (2)workProgress:正在执行的fiber,触发更新后，正在reconclier中计算的fiberNode树

  ### 3.fiberNode结构解读:
  一个fiber指一个将要执行或者已经执行结束的工作单元work。**一个组件可以有一个或者多个fiber**。
  ```js
    // fiber节点是链表结构
    class FiberNode {
      tag:WorkTag; // 标记fiber的类型，即描述的组件类型，如原生标签，函数组件，类组件，Fragment等
      key:Key; // 标记组件在当前层级下的唯一性,diff优化标识
      elementType: any; // 组件类型
      type:any; // 标记组件类型：原生组件是字符串（比如div），函数组件是函数，类组件是类

      return:FiberNode | null; // 父节点，构成双向链表
      child: FiberNode | null; // 子节点
      sibling:FiberNode | null; // 下一个兄弟节点
      index:number; // 记录节点在当前层级中的位置下标，diff时用来判断节点是否需要发生移动
      
      pendingProps:Props; // 新的props
      memoizedProps:Props | null; // 上一次渲染是使用的props

      updateQueue:unknown; // 任务队列，存储更新的callback,比如createRoot,render或者setState的更新

      memoizedState:{
        hooks: [state1, effectHook] // hooks状态（函数组件）
      }; // hook, state
      dependencies:any; // 依赖，比如context
      mode: any,// 模式

      flags:Flags; // 当前组件的阶段：渲染，更新等，update,noflags,placement,,,
      subTreeFlags:Flags;
      deletions:Array<Fiber> | null; // 记录要删除的子节点
      alternate:FiberNode | null; // 存储更新前的fiber

      stateNode:any;
      ref:Ref;
    }
  ```

  ### 4.FiberNode和VNode的区别
|     纬度     |                  FiberNode                   |                 VNode                        |
| :----------: | :-------------------------------------------:| :-------------------------------------------:|
|   设计目的   |   实现可中断的异步渲染 + 优先级调度lanes     |       减少真实 DOM 操作，提升渲染性能        |
|   数据结构   |            双向链表树（循环遍历              |               树形结构（递归遍历）           |
|   功能范围   |     描述 UI 结构 + 调度任务 + 副作用管理     |                 仅描述 UI 结构               |
|   遍历方式   |         循环遍历链表（可中断 + 恢复）        |                 递归遍历（不可中断）         |
|   任务调度   |              异步分片，空闲时间执行          |               同步执行，阻塞主线程           |
|  优先级控制  |           Lane 模型（31 个优先级车道）       |                        无                    |
|  副作用处理  |           构建副作用链表，分阶段提交         |                统一提交 DOM 更新             |

  ```js
    // vNode
    const vNode = {
      type: 'div', // 节点类型（组件/原生标签）
      props: { className: 'container' }, // 属性
      children: [vNode1, vNode2], // 子节点（树形结构）
      key: 'unique-id', // 优化 Diff 性能
      // 无状态、调度、副作用信息
    }
    // fiberNode
    const fiberNode = {
      tag: HostComponent, // 节点类型（函数组件/类组件/DOM元素）
      type: 'div', // 原生标签或组件构造函数
      key: 'unique-id', // Diff 优化标识
      stateNode: domNode, // 关联的真实 DOM 节点
      pendingProps: { className: 'container' }, // 待处理的 props
      memoizedProps: {}, // 已生效的 props
      memoizedState: {
        // Hooks 状态（函数组件）
        hooks: [state1, effectHook],
      },
      updateQueue: [], // 状态更新队列（类组件）
      lanes: Lanes.HighPriority, // 调度优先级（Lane 模型）
      child: childFiber, // 第一个子节点
      sibling: siblingFiber, // 下一个兄弟节点
      return: parentFiber, // 父节点（构成双向链表）
      effectTag: Placement, // 副作用标记（插入/更新/删除）
      nextEffect: nextEffectFiber, // 副作用链表指针
    }
  ```
  ### 5.FiberNode的Hooks状态管理
    ```js
      // 函数组件的 Hooks 链表
      fiberNode.memoizedState = {
        memoizedState: 'state value', // useState 的状态
        next: {
          // 下一个 Hook（如 useEffect）
          memoizedState: { cleanup: fn },
          next: null,
        },
      }
    ```
  ### 6.优先级调度
    ```js
      // 用户输入触发高优先级更新
      input.addEventListener('input', () => {
        React.startTransition(() => {
          setInputValue(e.target.value) // 低优先级
        })
        // 高优先级更新立即执行
      })
    ```
  ### 7.副作用批处理:
    ```js
      // 提交阶段遍历 effectList
      let nextEffect = fiberRoot.firstEffect
      while (nextEffect) {
        commitWork(nextEffect)
        nextEffect = nextEffect.nextEffect
      }
    ```


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


# 三：更新机制
  ### 1.常见触发更新的方式：
  - ReactDom.createRoot().render
  - this.setState
  - useState的dispatch
  ### 更新机制的组成部分
  - update：代表更新的数据结构
  - UpdateQueue:消费update的数据结构,UpdateQueue队列中包含多个sharePending,sharePending又是由多个update组成。
  ### 更新机制的工作流程
  - 实现mount时调用的API
  - 将该API接入上述更新机制中

fiberRootNode ----current----> hostRootFiber ----child----> APP ----return----> hostRootFiber ----stateNode----> fiberRootNode

# 四：首屏渲染的更新
# 五：初探mount流程
  更新流程的目的：生成wrip fiberNode树。
  进入A的beginWork --> 对比B的currentfiberNode和B的reactElement --> 生成B对应的Wrip 
  # multirepo和monorepo的区别
# react项目结构