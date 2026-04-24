# 一：scheduler和reconciler工作流程
  更新任务1,更新任务2(低优先级) -->  Scheduler(调度器)根据任务的优先级调度 --> Reconciler(协调器) --> Renderer(渲染器)

# ChildReconciler：协调子节点
  - deletions:FiberNode的属性记录要删除的子节点

# reconcileSingleElement
  - 协调单个节点，对于页面初次渲染，创建fiber，不涉及对比复用老节点
    ```js
      function reconcileSingleElement(
        returnFiber: FiberNode,
        currentFiber: FiberNode | null,
        element:ReactElementType
      ){
        const key = element.key
        work:
        if(currentFiber !== null) {
          if(currentFiber.key === key) {
            if(element.$$typeof === REACT_ELEMENT_TYPE){
              if(currentFiber.type === element.type){
                let props = element.props
                if(element.type === REACT_FRAGMENT_TYPE){
                  props = element.props.children
                }
                // type相同
                const existing = useFiber(currentFiber, element.props)
                existing.return = returnFiber
                // 当前节点可复用，标记剩下的节点删除
                deleteRemainingChildren(returnFiber, currentFiber)
                return existing
              }
              // key相同，type不同时删掉旧的
              deleteChild(returnFiber, currentFiber)
              break work
            } else {
              if(__DEN__){
                console.warn('还未实现的react类型,element')
                break work
              }
            }
          } else {
            // 删掉旧的
            deleteChild(returnFiber, currentFiber)
          }
        }
        let fiber 
        if(element.type === REACT_FRAGMENT_TYPE) {
          fiber = createFiberFromFragment(element.props.children, key)
        } else {
          fiber = createFiberFromElement(element)
        }
        fiber.return = returnFiber;
        return fiber;
      }
    ```

  ### deleteChild:删除子节点
    ```js
      function deleteChild (returnFiber:FiberNode, childToDelete:FiberNode) {
        if(!shouldTrackEffects){
          return
        }
        const deletions = returnFiber.deletions
        if(deletions === null){
          returnFiber.deletions = [childToDelete]
          returnFiber.flags |= ChildDeletion
        } else {
          deletions.push(childToDelete)
        }
      }
    ```
# commitDeletions：根据fiber删除dom节点