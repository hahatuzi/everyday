# commit
  > 遍历副作用链表，执行 DOM 操作和生命周期方法。
workLoop --> performUnitOfWork --> beginWork --> completeUnitOfWork --> commitRoot --> commitMutationEffects --> commitMutationEffectsOnFiber -->  