# Context
  beginWork --> updateContextProvider --> pushProvider --> complateWork --> popProvider
  ```js
  // 1.记录value,context, 2.后代组件消费，
  function updateContextProvider(
      current: Fiber | null,
      workInProgress: Fiber,
      renderLanes: Lanes,
    ) {
      const providerType: ReactProviderType<any> = workInProgress.type;
      const context: ReactContext<any> = providerType._context;

      const newProps = workInProgress.pendingProps;
      const oldProps = workInProgress.memoizedProps;

      const newValue = newProps.value;

      if (__DEV__) {
        if (!('value' in newProps)) {
          if (!hasWarnedAboutUsingNoValuePropOnContextProvider) {
            hasWarnedAboutUsingNoValuePropOnContextProvider = true;
            console.error(
              'The `value` prop is required for the `<Context.Provider>`. Did you misspell it or forget to pass it?',
            );
          }
        }
        const providerPropTypes = workInProgress.type.propTypes;

        if (providerPropTypes) {
          checkPropTypes(providerPropTypes, newProps, 'prop', 'Context.Provider');
        }
      }

      pushProvider(workInProgress, context, newValue);

      if (enableLazyContextPropagation) {
        // In the lazy propagation implementation, we don't scan for matching
        // consumers until something bails out, because until something bails out
        // we're going to visit those nodes, anyway. The trade-off is that it shifts
        // responsibility to the consumer to track whether something has changed.
      } else {
        if (oldProps !== null) {
          const oldValue = oldProps.value;
          if (is(oldValue, newValue)) {
            // No change. Bailout early if children are the same.
            if (
              oldProps.children === newProps.children &&
              !hasLegacyContextChanged()
            ) {
              return bailoutOnAlreadyFinishedWork(
                current,
                workInProgress,
                renderLanes,
              );
            }
          } else {
            // The context value changed. Search for matching consumers and schedule
            // them to update.
            propagateContextChange(workInProgress, context, renderLanes);
          }
        }
      }

      const newChildren = newProps.children;
      reconcileChildren(current, workInProgress, newChildren, renderLanes);
      return workInProgress.child;
    }
  ```

  ### Consumer
    ```js
      function updateContextConsumer(
        current: Fiber | null,
        workInProgress: Fiber,
        renderLanes: Lanes,
      ) {
        let context: ReactContext<any> = workInProgress.type;

        const newProps = workInProgress.pendingProps;
        const render = newProps.children;

        prepareToReadContext(workInProgress, renderLanes);
        const newValue = readContext(context);
        if (enableSchedulingProfiler) {
          markComponentRenderStarted(workInProgress);
        }
        let newChildren;
 
        newChildren = render(newValue);

        workInProgress.flags |= PerformedWork;
        reconcileChildren(current, workInProgress, newChildren, renderLanes);
        return workInProgress.child;
      }
    ```