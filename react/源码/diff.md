# diff
  > 老节点还有，新节点没了，删除剩余老节点
  > 新节点有，老节点没，新节点直接新增
  > 新老节点都有
  ```js
    // old: 0 1 2 3 4 5
    // new: 1 3 2 4 5
      function reconcileChildrenArray(
        returnFiber: Fiber,
        currentFirstChild: Fiber | null,
        newChildren: Array<*>,
        lanes: Lanes,
      ): Fiber | null {

        let resultingFirstChild: Fiber | null = null;
        let previousNewFiber: Fiber | null = null;

        let oldFiber = currentFirstChild;
        let lastPlacedIndex = 0;
        let newIdx = 0;
        let nextOldFiber = null;
        for (; oldFiber !== null && newIdx < newChildren.length; newIdx++) {
          if (oldFiber.index > newIdx) {
            nextOldFiber = oldFiber;
            oldFiber = null;
          } else {
            nextOldFiber = oldFiber.sibling;
          }
          const newFiber = updateSlot(
            returnFiber,
            oldFiber,
            newChildren[newIdx],
            lanes,
          );
          if (newFiber === null) {
            // TODO: This breaks on empty slots like null children. That's
            // unfortunate because it triggers the slow path all the time. We need
            // a better way to communicate whether this was a miss or null,
            // boolean, undefined, etc.
            if (oldFiber === null) {
              oldFiber = nextOldFiber;
            }
            break;
          }
          if (shouldTrackSideEffects) {
            if (oldFiber && newFiber.alternate === null) {
              // We matched the slot, but we didn't reuse the existing fiber, so we
              // need to delete the existing child.
              deleteChild(returnFiber, oldFiber);
            }
          }
          lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);
          if (previousNewFiber === null) {
            // TODO: Move out of the loop. This only happens for the first run.
            resultingFirstChild = newFiber;
          } else {
            // TODO: Defer siblings if we're not at the right index for this slot.
            // I.e. if we had null values before, then we want to defer this
            // for each null value. However, we also don't want to call updateSlot
            // with the previous one.
            previousNewFiber.sibling = newFiber;
          }
          previousNewFiber = newFiber;
          oldFiber = nextOldFiber;
        }

        if (newIdx === newChildren.length) {
          // We've reached the end of the new children. We can delete the rest.
          deleteRemainingChildren(returnFiber, oldFiber);
          if (getIsHydrating()) {
            const numberOfForks = newIdx;
            pushTreeFork(returnFiber, numberOfForks);
          }
          return resultingFirstChild;
        }

        if (oldFiber === null) {
          // If we don't have any more existing children we can choose a fast path
          // since the rest will all be insertions.
          for (; newIdx < newChildren.length; newIdx++) {
            const newFiber = createChild(returnFiber, newChildren[newIdx], lanes);
            if (newFiber === null) {
              continue;
            }
            lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);
            if (previousNewFiber === null) {
              // TODO: Move out of the loop. This only happens for the first run.
              resultingFirstChild = newFiber;
            } else {
              previousNewFiber.sibling = newFiber;
            }
            previousNewFiber = newFiber;
          }
          if (getIsHydrating()) {
            const numberOfForks = newIdx;
            pushTreeFork(returnFiber, numberOfForks);
          }
          return resultingFirstChild;
        }
        // 新老节点都有
        // 1 2 3 4 5
        // 1 2 3 5
        // Add all children to a key map for quick lookups.
        // 老节点生成Map结构数据
        const existingChildren = mapRemainingChildren(returnFiber, oldFiber);
        for (; newIdx < newChildren.length; newIdx++) {
          const newFiber = updateFromMap(
            existingChildren,
            returnFiber,
            newIdx,
            newChildren[newIdx],
            lanes,
          );
          if (newFiber !== null) {
            if (shouldTrackSideEffects) {
              if (newFiber.alternate !== null) {
                // The new fiber is a work in progress, but if there exists a
                // current, that means that we reused the fiber. We need to delete
                // it from the child list so that we don't add it to the deletion
                // list.
                existingChildren.delete(
                  newFiber.key === null ? newIdx : newFiber.key,
                );
              }
            }
            lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);
            if (previousNewFiber === null) {
              resultingFirstChild = newFiber;
            } else {
              previousNewFiber.sibling = newFiber;
            }
            previousNewFiber = newFiber;
          }
        }
        // 新fiber构建完成了，但是老fiber还未删除
        if (shouldTrackSideEffects) {
          existingChildren.forEach(child => deleteChild(returnFiber, child));
        }

        if (getIsHydrating()) {
          const numberOfForks = newIdx;
          pushTreeFork(returnFiber, numberOfForks);
        }
        return resultingFirstChild;
      }
      function mapRemainingChildren(
        returnFiber: Fiber,
        currentFirstChild: Fiber,
      ): Map<string | number, Fiber> {
        const existingChildren: Map<string | number, Fiber> = new Map();

        let existingChild = currentFirstChild;
        while (existingChild !== null) {
          if (existingChild.key !== null) {
            existingChildren.set(existingChild.key, existingChild);
          } else {
            existingChildren.set(existingChild.index, existingChild);
          }
          existingChild = existingChild.sibling;
        }
        return existingChildren;
      }

      function deleteChild(returnFiber: Fiber, childToDelete: Fiber): void {
        if (!shouldTrackSideEffects) {
          // Noop.
          return;
        }
        const deletions = returnFiber.deletions;
        if (deletions === null) {
          returnFiber.deletions = [childToDelete];
          returnFiber.flags |= ChildDeletion;
        } else {
          deletions.push(childToDelete);
        }
      }
  ```
  ### updateTextNode
    ```js
    function updateTextNode(
        returnFiber: Fiber,
        current: Fiber | null,
        textContent: string,
        lanes: Lanes,
      ) {
        if (current === null || current.tag !== HostText) {
          // Insert
          const created = createFiberFromText(textContent, returnFiber.mode, lanes);
          created.return = returnFiber;
          return created;
        } else {
          // Update
          const existing = useFiber(current, textContent);
          existing.return = returnFiber;
          return existing;
        }
      }
    ```

# react和vue3的diff比较
  > new vdom是文本 --> old dom是数组，不匹配，删除老节点
                   --> old dom是文本，更新修改
  > new vdom是数组 --> old dom是数组 --> 左边按需查找，如果节点不能复用，停止
                                     --> 右边按需查找，如果节点不能复用，停止（vue有从右边查找该步骤，react无）
                                     --> 老节点没有，新节点有，直接新增
                                     --> 新节点没有，老节点有，直接删除
                                     --> 新老节点都有，但是涉及移动节点时 --> vue是数组形式（遍历新老节点进行移动，复用等操作），react是key,value形式的Map结构，