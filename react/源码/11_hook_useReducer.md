# useReducer
  > useReducer --> updateReducer --> 
  ```js
    useReducer<S, I, A>(
      reducer: (S, A) => S,
      initialArg: I,
      init?: I => S,
    ): [S, Dispatch<A>] {
      currentHookNameInDev = 'useReducer';
      mountHookTypesDev();
      const prevDispatcher = ReactCurrentDispatcher.current;
      ReactCurrentDispatcher.current = InvalidNestedHooksDispatcherOnMountInDEV;
      try {
        return mountReducer(reducer, initialArg, init);
      } finally {
        ReactCurrentDispatcher.current = prevDispatcher;
      }
    },
    function mountReducer<S, I, A>(
      reducer: (S, A) => S,
      initialArg: I,
      init?: I => S,
    ): [S, Dispatch<A>] {
      // 构建hook链表（mount,update)
      const hook = mountWorkInProgressHook();
      let initialState;
      if (init !== undefined) {
        initialState = init(initialArg);
      } else {
        initialState = ((initialArg: any): S);
      }
      // 初始值存储
      hook.memoizedState = hook.baseState = initialState;
      const queue: UpdateQueue<S, A> = {
        pending: null,
        lanes: NoLanes,
        dispatch: null,
        lastRenderedReducer: reducer,
        lastRenderedState: (initialState: any),
      };
      hook.queue = queue;
      // dispatch
      const dispatch: Dispatch<A> = (queue.dispatch = (dispatchReducerAction.bind(
        null,
        currentlyRenderingFiber,
        queue,
      ): any));
      return [hook.memoizedState, dispatch];
    }

    export type UpdateQueue<S, A> = {|
      pending: Update<S, A> | null,
      lanes: Lanes,
      dispatch: (A => mixed) | null,
      lastRenderedReducer: ((S, A) => S) | null,
      lastRenderedState: S | null,
    |};
    function dispatchReducerAction<S, A>(
      fiber: Fiber,
      queue: UpdateQueue<S, A>,
      action: A,
    ) {
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
        const root = enqueueConcurrentHookUpdate(fiber, queue, update, lane);
        if (root !== null) {
          const eventTime = requestEventTime();
          scheduleUpdateOnFiber(root, fiber, lane, eventTime);
          entangleTransitionUpdate(root, queue, lane);
        }
      }

      markUpdateInDevTools(fiber, lane, action);
    }
  ```
  ### updateReducer
  ```js
    function updateReducer<S, I, A>(
      reducer: (S, A) => S,
      initialArg: I,
      init?: I => S,
    ): [S, Dispatch<A>] {
      const hook = updateWorkInProgressHook();
      const queue = hook.queue;
      queue.lastRenderedReducer = reducer;

      const current: Hook = (currentHook: any);

      let baseQueue = current.baseQueue;
      const pendingQueue = queue.pending;
      if (pendingQueue !== null) {
        if (baseQueue !== null) {
          const baseFirst = baseQueue.next;
          const pendingFirst = pendingQueue.next;
          baseQueue.next = pendingFirst;
          pendingQueue.next = baseFirst;
        }
        current.baseQueue = baseQueue = pendingQueue;
        queue.pending = null;
      }

      if (baseQueue !== null) {
        const first = baseQueue.next;
        let newState = current.baseState;

        let newBaseState = null;
        let newBaseQueueFirst = null;
        let newBaseQueueLast = null;
        let update = first;
        do {
          const updateLane = removeLanes(update.lane, OffscreenLane);
          const isHiddenUpdate = updateLane !== update.lane;

          const shouldSkipUpdate = isHiddenUpdate
            ? !isSubsetOfLanes(getWorkInProgressRootRenderLanes(), updateLane)
            : !isSubsetOfLanes(renderLanes, updateLane);

          if (shouldSkipUpdate) {
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
            currentlyRenderingFiber.lanes = mergeLanes(
              currentlyRenderingFiber.lanes,
              updateLane,
            );
            markSkippedUpdateLanes(updateLane);
          } else {
            // This update does have sufficient priority.

            if (newBaseQueueLast !== null) {
              const clone: Update<S, A> = {
                lane: NoLane,
                action: update.action,
                hasEagerState: update.hasEagerState,
                eagerState: update.eagerState,
                next: (null: any),
              };
              newBaseQueueLast = newBaseQueueLast.next = clone;
            }
            if (update.hasEagerState) {
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

        if (!is(newState, hook.memoizedState)) {
          markWorkInProgressReceivedUpdate();
        }

        hook.memoizedState = newState;
        hook.baseState = newBaseState;
        hook.baseQueue = newBaseQueueLast;

        queue.lastRenderedState = newState;
      }

      if (baseQueue === null) {
        // `queue.lanes` is used for entangling transitions. We can set it back to
        // zero once the queue is empty.
        queue.lanes = NoLanes;
      }

      const dispatch: Dispatch<A> = (queue.dispatch: any);
      return [hook.memoizedState, dispatch];
    }

  ```