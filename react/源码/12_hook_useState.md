# 一：useState
  ### 1.工作流程：
  useState --> dispatcher.useState() --> resolveDispatcher() --> ReactCurentDispatcher.current --> HooksDispatcherOnmount/ HooksDispatcherOnUpdate
  --> mountWorkInProgressHook() --> hook --> queue --> dispatchSetState --> requestUpdateLan(fiber) --> enqueueConCurrentHookUpdate() -->
  scheduleUpdateOnFiber(root,  fiber,  lane, eventTime),entangTransitionUpdate(root, queue, lane)
  ### 2.代码分析：
  mountWorkInProgressHook --> basicStateReducer --> 
  - (1)useState需要实现：
    - 针对update的dispatcher
    - 实现对标mountWorkInProgress的updateWorkInProgressHook
    - 实现updateState中的计算新state的逻辑
  - (2)其中updateWorkInProgress的实现需要考虑的问题：
    - hook数据从哪里来？
    - 交互阶段触发的更新
    ```js
      const [age, setAge] = useState(1)
      function increment () {
        setAge(age + 1)
      }
      <button onClick={() => {
        increment()
        increment()
        increment()
      }}></button>
      // 2,setAge多次调用，会进行合并，最终只触发一次更新，如果想要调用多次，可以改成setAge(age => age + 1)
    ```
  
# 二：useState的mount和update流程的区别
  ### beginWork：
  - 需要处理childDeletion的情况
  - 需要处理节点移动的情况
  ### completeWork：
  - 需要处理HostText内容更新的情况
  - 需要处理HostComponent属性变化的情况
  ### commitWork:
  - 对于ChildDeletion,需要遍历被删除的子树
  ### useState：
  - 实现相对于mountState的updateState

# 三：源码
  ```js
    function mountState<State>(initialState:(()=> State | State)):[State,Dispatch<State>]{
      const hook = mountWorkInprogressHook()
      let memoizedState
      // 初始值可以是函数
      if(initialState instanceof Function){
        memoizedState = initialState()
      } else {
        memoizedState = initialState
      }

      const queue = createUpdateQueue<State>()
      hook.updateQueue = queue

      const dispatch = dispatchSetState.bind(null, currentlyRenderingFiber, queue)
      queue.dispatch = dispatch
      return [memoizedState, dispatch]
    }
    function dispatchSetState<S, A>( fiber: Fiber, queue: UpdateQueue<S, A>, action: A,) {

      const lane = requestUpdateLane(fiber);

      const update: Update<S, A> = {
        lane,
        action,
        hasEagerState: false,
        eagerState: null,
        next: (null: any),
      };

      if (isRenderPhaseUpdate(fiber)) {
        enqueueRenderPhaseUpdate(queue, update);
      } else {
        const alternate = fiber.alternate;
        if (
          fiber.lanes === NoLanes &&
          (alternate === null || alternate.lanes === NoLanes)
        ) {
          const lastRenderedReducer = queue.lastRenderedReducer;
          if (lastRenderedReducer !== null) {
            let prevDispatcher;
            if (__DEV__) {
              prevDispatcher = ReactCurrentDispatcher.current;
              ReactCurrentDispatcher.current = InvalidNestedHooksDispatcherOnUpdateInDEV;
            }
            try {
              const currentState: S = (queue.lastRenderedState: any);
              const eagerState = lastRenderedReducer(currentState, action);
              update.hasEagerState = true;
              update.eagerState = eagerState;
              // 如果state没变，组件不做更新，而useReducer还是会让函数组件更新
              if (is(eagerState, currentState)) {
                enqueueConcurrentHookUpdateAndEagerlyBailout(
                  fiber,
                  queue,
                  update,
                  lane,
                );
                return;
              }
            } catch (error) {
              // Suppress the error. It will throw again in the render phase.
            } finally {
              if (__DEV__) {
                ReactCurrentDispatcher.current = prevDispatcher;
              }
            }
          }
        }

        const root = enqueueConcurrentHookUpdate(fiber, queue, update, lane);
        if (root !== null) {
          const eventTime = requestEventTime();
          scheduleUpdateOnFiber(root, fiber, lane, eventTime);
          entangleTransitionUpdate(root, queue, lane);
        }
      }

      markUpdateInDevTools(fiber, lane, action);
    }


    function updateState<S>( initialState: (() => S) | S, ): [S, Dispatch<BasicStateAction<S>>] {
      return updateReducer(basicStateReducer, (initialState: any));
    }
    function updateReducer<S, I, A>(
      reducer: (S, A) => S,
      initialArg: I,
      init?: I => S,
    ): [S, Dispatch<A>] {
      const hook = updateWorkInProgressHook();
      const queue = hook.queue;

      if (queue === null) {
        throw new Error(
          'Should have a queue. This is likely a bug in React. Please file an issue.',
        );
      }

      queue.lastRenderedReducer = reducer;

      const current: Hook = (currentHook: any);

      // The last rebase update that is NOT part of the base state.
      let baseQueue = current.baseQueue;

      // The last pending update that hasn't been processed yet.
      const pendingQueue = queue.pending;
      if (pendingQueue !== null) {
        // We have new updates that haven't been processed yet.
        // We'll add them to the base queue.
        if (baseQueue !== null) {
          // Merge the pending queue and the base queue.
          const baseFirst = baseQueue.next;
          const pendingFirst = pendingQueue.next;
          baseQueue.next = pendingFirst;
          pendingQueue.next = baseFirst;
        }
        current.baseQueue = baseQueue = pendingQueue;
        queue.pending = null;
      }

      if (baseQueue !== null) {
        // We have a queue to process.
        const first = baseQueue.next;
        let newState = current.baseState;

        let newBaseState = null;
        let newBaseQueueFirst = null;
        let newBaseQueueLast = null;
        let update = first;
        do {
          const updateLane = update.lane;
          if (!isSubsetOfLanes(renderLanes, updateLane)) {
            // Priority is insufficient. Skip this update. If this is the first
            // skipped update, the previous update/state is the new base
            // update/state.
            const clone: Update<S, A> = {
              lane: updateLane,
              action: update.action,
              hasEagerState: update.hasEagerState,
              eagerState: update.eagerState,
              next: (null: any),
            };
            if (newBaseQueueLast === null) {
              newBaseQueueFirst = newBaseQueueLast = clone;
              newBaseState = newState;
            } else {
              newBaseQueueLast = newBaseQueueLast.next = clone;
            }
            // Update the remaining priority in the queue.
            // TODO: Don't need to accumulate this. Instead, we can remove
            // renderLanes from the original lanes.
            currentlyRenderingFiber.lanes = mergeLanes(
              currentlyRenderingFiber.lanes,
              updateLane,
            );
            markSkippedUpdateLanes(updateLane);
          } else {
            // This update does have sufficient priority.

            if (newBaseQueueLast !== null) {
              const clone: Update<S, A> = {
                // This update is going to be committed so we never want uncommit
                // it. Using NoLane works because 0 is a subset of all bitmasks, so
                // this will never be skipped by the check above.
                lane: NoLane,
                action: update.action,
                hasEagerState: update.hasEagerState,
                eagerState: update.eagerState,
                next: (null: any),
              };
              newBaseQueueLast = newBaseQueueLast.next = clone;
            }

            // Process this update.
            if (update.hasEagerState) {
              // If this update is a state update (not a reducer) and was processed eagerly,
              // we can use the eagerly computed state
              newState = ((update.eagerState: any): S);
            } else {
              const action = update.action;
              newState = reducer(newState, action);
            }
          }
          update = update.next;
        } while (update !== null && update !== first);

        if (newBaseQueueLast === null) {
          newBaseState = newState;
        } else {
          newBaseQueueLast.next = (newBaseQueueFirst: any);
        }

        // Mark that the fiber performed work, but only if the new state is
        // different from the current state.
        if (!is(newState, hook.memoizedState)) {
          markWorkInProgressReceivedUpdate();
        }

        hook.memoizedState = newState;
        hook.baseState = newBaseState;
        hook.baseQueue = newBaseQueueLast;

        queue.lastRenderedState = newState;
      }

      // Interleaved updates are stored on a separate queue. We aren't going to
      // process them during this render, but we do need to track which lanes
      // are remaining.
      const lastInterleaved = queue.interleaved;
      if (lastInterleaved !== null) {
        let interleaved = lastInterleaved;
        do {
          const interleavedLane = interleaved.lane;
          currentlyRenderingFiber.lanes = mergeLanes(
            currentlyRenderingFiber.lanes,
            interleavedLane,
          );
          markSkippedUpdateLanes(interleavedLane);
          interleaved = ((interleaved: any).next: Update<S, A>);
        } while (interleaved !== lastInterleaved);
      } else if (baseQueue === null) {
        // `queue.lanes` is used for entangling transitions. We can set it back to
        // zero once the queue is empty.
        queue.lanes = NoLanes;
      }

      const dispatch: Dispatch<A> = (queue.dispatch: any);
      return [hook.memoizedState, dispatch];
    }
  ```

```js
const queue = []
let index = 0
const useState = (initialState) => {
  queue.push(initialState)
  const update = (0 => {
    queue.push(state)
    index++
  })
  return [queue[index], update]
}
```