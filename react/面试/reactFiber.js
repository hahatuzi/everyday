// ===============任务相关=================
// 任务队列
const taskQueue = []

// 将任务添加至任务队列
function schedule (task) {
  taskQueue.push(task)
}
// 模拟任务并处理任务
const exampleTask = {
  element:["div", 'p','span']
}
// 启动任务并更新fiber
schedule(exampleTask)
updateFiberTree()
// ===============fiber处理=================
// 需要通过fiber存储一些信息，根fiber
const rootfiber = null
// 正在工作的fiber
const currentFiber = null
// 首先创建一个fiber,模拟mount的时候创建的fiber
function createFiber(element,parentFiber){
  return {
    element,
    parent:parentFiber,
    child:null,
    sibling:null
  }
}
// fiber更新的方法
function updateFiberTree () {
  if(!rootFiber){
    rootFiber = createFIber('App', null)
    currentFiber = rootFiber
  }

  // 任务队列中有任务
  while (taskQueue.length > 0) {
    const task = taskQueue.shift()
    // 做对应的工作
  }
  // 执行任务单元
  function performUnitOfWork (fiber) {
    // 执行当前任务，并且返回下一个任务
    const elements = fiber.element
    // 1.判断elements是否有子fiber
    if(elements && elements.length > 0){
      let child = null
      elements.forEach((element,index) => {
        const newFiber = createFiber(element,fiber)
        if(index == 0){
          fiber.child = newFiber
        } else {
          child.sibling = newFiber
        }
        child = newFiber
      })
    }
    // 如果有子节点，直接返回第一个子节点
    if(fiber.child){
      return fiber.child
    }
    let nextFiber = fiber
    while(nextFiber){
      if(nextFiber.sibling){
        return nextFiber.sibling
      }
      nextFiber = nextFiber.parent
    }

    return null
  }
}

// 提交fiber的改动
function commitRoot () {
  commitWorker(rootFiber.child)
  currentFiber = null
}

function commitWorker(fiber){
  if(!fiber) {
    return
  }

  commitWorker(fiber.child)
  commitWorker(fiber.sibling)
}
