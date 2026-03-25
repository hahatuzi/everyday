# Hooks的原理：
  > Hooks的底层机制其实就是使用**链表结构**存储hook
  > React通过currentlyRenderingFIber和workInProgressHook来追踪Hook的调用顺序。
  > workInProgressHook:当前正在工作的hook,是hook链表中的一个节点。
  > currentlyRenderingFiber: "当前渲染组件"的指针
  > resolveCurrentlyRenderingFiber:获取当前Fiber的节点
  > fiber.memorizedState(hook1) --> next(hook2) --> next(hook3)
  ### 工作流程
  beginWork --> updateFunctionComponent --> renderWithHooks --> HooksDispatcherOnMount/HooksDispatcherOnUpdate --> mountWorkInprogressHook/updateWorkInProgressHook
  ### workInProgressHook
    ```js
      interface Hook {
        memoizedState:any;
        updateQueue:unknown;
        next:Hook | null;
      }
      let workInProgressHook : Hook | null
    ```
  ### mountWorkInprogressHook
    ```js
      function mountWorkInprogressHook():Hook{
        const hook:Hook = {
          memoizedState:null,
          updateQueue:null,
          next:null
        }
        if(workInprogressHook === null){
          // mount时第一个hook
          if(currentlyRenderingFiber === null){
            throw new Error('请在函数组件内调用hook')
          } else {
            workInprogressHook = hook
          }
        } else {
          workInprogressHook.next = hook
          workInprogressHook = hook
        }
      }
    ```
  ### updateWorkInProgressHook
    ```js
       // 1.返回当前useXX函数对应的hook
      // 2.构建hook链表
      function updateWorkInProgressHook ():Hook {
        let nextCurrentHook: Hook | null;
        if (currentHook === null) {
          // update阶段
          // FC update时的第一个hook
          const current = currentlyRenderingFiber?.alternate
          if(current !== null){
            nextCurrentHook = current?.memoizedState
          } else {
            nextCurrentHook = null
          }
        } else {
        // mount阶段
          nextCurrentHook = currentHook.next
        }

        if (nextCurrentHook === null){
          throw new Error(`组件${currentlyRenderingFiber?.type}本次执行时的hook比上次多`)
        }

        const newHook: Hook = {
          memoizedState: currentHook?.memoizedState,
          updateQueue: currentHook?.updateQueue,
          next:null
        }

        if(workInprogressHook === null){
          // mount时第一个hook
          if(currentlyRenderingFiber === null){
            throw new Error('请在函数组件内调用hook')
          } else {
            workInprogressHook = newHook
            currentlyRenderingFiber.memoizedState = workInprogressHook.memoizedState
          }
        } else {
        // hook链表的头结点
          workInprogressHook.next = newHook
          workInprogressHook = newHook
        }
        return workInprogressHook
      }
    ```