# 一：useLayoutEffect(create, )
  
  ### 源码
    ```js
      function mountLayoutEffect(
        create: () => (() => void) | void,
        deps: Array<mixed> | void | null,
      ): void {
        let fiberFlags: Flags = UpdateEffect;
        if (enableSuspenseLayoutEffectSemantics) {
          fiberFlags |= LayoutStaticEffect;
        }
        if (
          __DEV__ &&
          enableStrictEffects &&
          (currentlyRenderingFiber.mode & StrictEffectsMode) !== NoMode
        ) {
          fiberFlags |= MountLayoutDevEffect;
        }
        return mountEffectImpl(fiberFlags, HookLayout, create, deps);
      }

      function updateLayoutEffect(
        create: () => (() => void) | void,
        deps: Array<mixed> | void | null,
      ): void {
        return updateEffectImpl(UpdateEffect, HookLayout, create, deps);
      }

      function mountEffectImpl(fiberFlags, hookFlags, create, deps): void {
        const hook = mountWorkInProgressHook();
        const nextDeps = deps === undefined ? null : deps;
        currentlyRenderingFiber.flags |= fiberFlags;
        // 1.保存effect2.构建effect链表
        hook.memoizedState = pushEffect(
          HookHasEffect | hookFlags,
          create,
          undefined,
          nextDeps,
        );
      }

      function updateEffectImpl(fiberFlags, hookFlags, create, deps): void {
        const hook = updateWorkInProgressHook();
        const nextDeps = deps === undefined ? null : deps;
        let destroy = undefined;

        if (currentHook !== null) {
          const prevEffect = currentHook.memoizedState;
          destroy = prevEffect.destroy;
          // 依赖项是否发生变化
          if (nextDeps !== null) {
            const prevDeps = prevEffect.deps;
            if (areHookInputsEqual(nextDeps, prevDeps)) {
              hook.memoizedState = pushEffect(hookFlags, create, destroy, nextDeps);
              return;
            }
          }
        }

        currentlyRenderingFiber.flags |= fiberFlags;
        hook.memoizedState = pushEffect(
          HookHasEffect | hookFlags,
          create,
          destroy,
          nextDeps,
        );
      }
    ```
  ### 应用场景
    ```js
     
    ```

# 二：useEffect 和 useLayoutEffect 的区别
  > useEffect:组件更新挂载完成后 VDOM --> DOM 更新 --> useEffect :造成页面闪动
  > useLayoutEffect:组件更新挂载完成后 VDOM --> useLayoutEffect --> DOM 更新 : 造成页面卡顿
  > useLayoutEffect **内部的代码和所有计划的状态更新阻塞了浏览器重新绘制屏幕**。如果过度使用，这会使你的应用程序变慢。如果可能的话，尽量选择 useEffect。
|         阶段        |                       useEffect                | useLayoutEffect  |
| :-----------------: | :---------------------------------------------:| :---------------:|
| beforeMutation阶段  |                 调度flushPassiveEffects        |        无        |
|    mutation阶段     |                           无                   |   执行destory    |
|     layout阶段      |                 注册destory，create            |   执行create     |
|  commit阶段完成后   |   注册flushPassiveEffects,内部执行注册的回调   |        无        |