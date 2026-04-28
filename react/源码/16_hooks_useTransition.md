# useTransition
  ```js
    function mountTransition(): [ boolean, (callback: () => void, options?: StartTransitionOptions) => void,] {
      const [isPending, setPending] = mountState(false);
      // The `start` method never changes.
      const start = startTransition.bind(null, setPending);
      const hook = mountWorkInProgressHook();
      hook.memoizedState = start;
      return [isPending, start];
    }

    function updateTransition(): [ boolean, (callback: () => void, options?: StartTransitionOptions) => void,] {
      const [isPending] = updateState(false);
      const hook = updateWorkInProgressHook();
      const start = hook.memoizedState;
      return [isPending, start];
    }

    function startTransition(setPending, callback, options) {
      const previousPriority = getCurrentUpdatePriority();
      setCurrentUpdatePriority(
        higherEventPriority(previousPriority, ContinuousEventPriority),
      );

      setPending(true);

      const prevTransition = ReactCurrentBatchConfig.transition;
      ReactCurrentBatchConfig.transition = {};
      const currentTransition = ReactCurrentBatchConfig.transition;

      if (enableTransitionTracing) {
        if (options !== undefined && options.name !== undefined) {
          ReactCurrentBatchConfig.transition.name = options.name;
          ReactCurrentBatchConfig.transition.startTime = now();
        }
      }
      try {
        setPending(false);
        callback();
      } finally {
        setCurrentUpdatePriority(previousPriority);

        ReactCurrentBatchConfig.transition = prevTransition;

        if (__DEV__) {
          if (prevTransition === null && currentTransition._updatedFibers) {
            const updatedFibersCount = currentTransition._updatedFibers.size;
            if (updatedFibersCount > 10) {
              console.warn(
                'Detected a large number of updates inside startTransition. ' +
                  'If this is due to a subscription please re-write it to use React provided hooks. ' +
                  'Otherwise concurrent mode guarantees are off the table.',
              );
            }
            currentTransition._updatedFibers.clear();
          }
        }
      }
    }
  ```