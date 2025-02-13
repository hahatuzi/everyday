import TodoTemplate from "./TodoTemplate"
import { ITodoData } from "./typings"
import { createItem, findParentNode } from "./utils"

class TodoDom extends TodoTemplate {
  private todoWrapper: HTMLElement

  constructor(todoWrapper: HTMLElement) {
    super()
    this.todoWrapper = todoWrapper
  }

  protected initList (todoData:ITodoData[]) {
    if (todoData.length) {
      const oFrag: DocumentFragment = document.createDocumentFragment()
      todoData.map((item: ITodoData) => {
        const oItem:HTMLElement = createItem('div', 'todo-item', this.todoView(item))
        oFrag.appendChild(oItem)
        // const oItem: HTMLElement = document.createElement('div')
        // oItem.className = 'todo-item'
        // oItem.innerHTML = this.todoView(item)
      })
      this.todoWrapper.appendChild(oFrag)
    }
  }

  protected addItem (todo:ITodoData) {
    const oItem:HTMLElement = createItem('div', 'todo-item', this.todoView(todo))
        // const oItem:HTMLElement = document.createElement('div')
    // oItem.className = 'todo-item'
    // oItem.innerHTML = this.todoView(todo)
    
    this.todoWrapper.appendChild(oItem)
  }

  protected removeItem (target: HTMLElement) {
    const oParentNode: HTMLElement = findParentNode(target, 'todo-item')
    oParentNode.remove()
  }

  protected changeComplated (target: HTMLElement, completed: boolean) {
    const oParentNode: HTMLElement = findParentNode(target, 'todo-item')
    const oContent: any = oParentNode.getElementsByTagName('span')[0]
    
    oContent.style.textDecoration = completed ? 'line-through' : 'none'
  }
}

export default TodoDom