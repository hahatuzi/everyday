export function findParentNode (target: HTMLElement, className: string) {
  while (target = target.parentNode as HTMLElement) {
    if (target.className === className) {
      return target
    }
  }
}

export function createItem (target: string, className:string, todoItem: string) {
  const oItem:HTMLElement = document.createElement(target)
  oItem.className = className
  oItem.innerHTML = todoItem

  return oItem
}