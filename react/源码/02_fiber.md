# 一：Fiber
  > fiberNode是虚拟DOM在react中的实现方式。vue中叫VNode。
  > 旧版本react采用递归遍历虚拟DOM树，组件树庞大时比较好使，不能停止
  > 它介于React Element和真实UI节点之间，能够表达节点之间的关系，转换过程为JSX --> ReactElement --> FIberNode--> DomElement。
  ### 1.jsx和fiber的关系，ReactElement与fiber的关系对比,fiber的创建和更新
  ReactElement如果作为核心模块操作的数据结构，存在以下问题：
   - 无法表达节点之间的关系
   - 字段有限，不好扩展
  所以需要一种新的数据结构，也就是FiberNode。
  - **mount**时通过jsx对象（调用createElement的结果）调用**createFiberFromElement**生成Fiber
  - **update**时通过**reconcileChildFibers**或**reconcileChildrenArray**对比新jsx和老的Fiber（current Fiber）生成新的wip Fiber树

  ### 2.Fiber的特点
   - (1)**实现增量式渲染**：将耗时渲染工作拆分成多个块，并分散在多个帧上进行处理
   - (2)**可中断任务**：支持暂停，中止，或者复用工作单元work
   - (3)**优先级调度**：Scheduler调度器：给不同类型的work赋予优先级，immediate,user-blocking,normal, low,idle比如用户输入可以打断数据更新任务
      ```js
        // 用户输入触发高优先级更新
        input.addEventListener('input', () => {
          React.startTransition(() => {
            setInputValue(e.target.value) // 低优先级
          })
          // 高优先级更新立即执行
        })
      ```
   - (4)**并发模式基础**：为Suspense,useTransition等特性提供底层支持

  ### 3.Fiber分类(双缓存机制)
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

      updateQueue:unknown; // **UpdateQueue链表结构**，存储更新的callback,比如createRoot,render或者setState的更新

      memoizedState:{
        // 对于FC对应的fiberNode，存在两层数据：memoizedState对应Hooks链表
        hooks: [state1, effectHook] // hooks状态（函数组件）
      }; // hook, state
      dependencies:any; // 依赖，比如context
      mode: any,// 模式

      flags:Flags; // 当前组件的阶段：渲染，更新等，update,noflags,placement,,,
      subTreeFlags:Flags;
      deletions:Array<Fiber> | null; // 记录要删除的子节点
      alternate:FiberNode | null; // 存储更新前的fiber,缓存fiber

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

  ### 6.副作用批处理:
    ```js
      // 提交阶段遍历 effectList
      let nextEffect = fiberRoot.firstEffect
      while (nextEffect) {
        commitWork(nextEffect)
        nextEffect = nextEffect.nextEffect
      }
    ```
# 二：fiber的创建与更新
  ### 1.FiberRoot和HostRootFiber的区别
  - **FiberRoot:应用根容器**
    - 1.createContainer --> createFiberRoot --> FiberRoot = new FiberRootNode()
    - 2.接收所有更新（如 setState、root.render()
    - 3.计算更新优先级（Lane 模型），调度任务
    - 4.协调双缓存：创建**workInProgress**树，完成后用**current**指针切换。
    - 5.管理渲染进度、错误边界、挂起任务
  - **HostRootFiber:Fiber树的根节点，fiber树的起点**
    - 1.作为**beginWork**的起点，开始深度遍历构建FIber。
    - 2.处理自身的更新队列，计算最新状态。
    - 3.创建 / 更新 / 删除子节点（如 <App />）的 Fiber 节点。
    - 4.最终在**commit**阶段，将变化提交到真实DOM。
    ```js
      export function createFiberRoot(): FiberRoot {
        const root: FiberRoot = new FiberRootNode(
          containerInfo,
          tag,
          hydrate,
          identifierPrefix,
          onRecoverableError,
        )
        const uninitializedFiber = createHostRootFiber(
          tag,
          isStrictMode,
          concurrentUpdatesByDefaultOverride,
        )
        root.current = uninitializedFiber;
        uninitializedFiber.stateNode = root;
      }
      export function createHostRootFiber(
        tag: RootTag,
        isStrictMode: boolean,
        concurrentUpdatesByDefaultOverride: null | boolean,
      ): Fiber {
        return createFiber(HostRoot, null, null, mode);
      }
      const createFiber = function(
        tag: WorkTag,
        pendingProps: mixed,
        key: null | string,
        mode: TypeOfMode,
      ): Fiber {
        return new FiberNode(tag, pendingProps, key, mode);
      };
    ```

  ### 2.工作流程
  > 创建流程：ReactDOM.render --> createRoot --> createContainer(初始化更新队列initializeUpdateQueue) --> FiberRootNode -->  createHostRootFiber --> 初始化更新队列initializeUpdateQueue(fiber.updateQueue = queue)fiber的任务更新队列。
  > 更新流程：createRoot --> updateContainer(处理优先级更新队列) --> 创建更新对象createUpdate(lane,next,acion) --> 更新入队updateQueue
    ```js
      /**
       * createRoot,是页面渲染的入口函数，reactDOM.createRoot()内部执行createContainer，创建整个应用的根节点fiberrootNode
      *
      * @param {Container} container
      * @param {CreateRootOptions} options
      * @returns {RootType} reactDOMRoot的实例
      */
      function createRoot(container:Container, options?:CreateRootOptions): RootType{
        const root = createContainer(container)
        return {
          render(element:ReactElementType){
            initEvent(container, 'click')
            updateContainer(element,root)
          },
          unmount(),
          _internalroot
        }
      }
      // reactDOM.createRoot()内部执行createContainer，创建整个应用的根节点fiberRootNode
      export function createContainer(container:Container){
        const hostRootFiber= new FiberNode(HostRoot, {}, null)
        const root = new FiberRootNode(container, hostRootFiber)
        hostRootFiber.updateQueue = createUpdateQueue()
        return root
      }
      // reactDOM.createRoot().render执行updateContainer,将首屏渲染和更新机制联系在一起
      export function updateContainer(
        element:ReactElementType | null,
        root:FiberRootNode
      ){
        const hostRootFiber = root.current
        const lane = requestUpdateLane() // 页面初次渲染，defaultLane
        // 每一个update都会被分配一个或者多个lane,以确保他在更新队列中的优先级顺序
        const update = createUpdate<ReactElementType | null>(element, lane)
        enqueueUpdate(
          hostRootFiber.updateQueue as UpdateQueue<ReactElementType | null>,
          update
        )
        // 开始调度
        scheduleUpdateOnFiber(hostRootFiber)
        return element
      }
    ```