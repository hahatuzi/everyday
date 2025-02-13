import TodoDom from "./TodoDom";
import { getTodoList, removeTodo, toggleTodo, addTodo } from "./TodoServices";
import { ITodoData } from "./typings";

class TodoEvent extends TodoDom {

  private todoData:ITodoData[]

  constructor(todoData: ITodoData[], todoWrapper: HTMLElement) {
    super(todoWrapper)
    
    this.todoData = todoData
    this.init()
  }
  
  @getTodoList
  private init(todoData:ITodoData[]) {
    console.log(todoData);
    this.todoData = todoData
    this.initList(todoData)
    
  }
  // 新增数据
  @addTodo
  public addTodo (todo:ITodoData): undefined | number {
    const _todo = this.todoData.filter((item:ITodoData) => item.content == todo.content)[0]
    
    if (!_todo) {
      this.todoData.push(todo)
      this.addItem(todo)
      return
    }
    return 1001
  }

  // 删除数据
  @removeTodo
  public removeTodo (target: HTMLElement, id: number): void {
    this.todoData = this.todoData.filter((item:ITodoData) => { item.id != id})
    this.removeItem(target)
  }

  // 更新数据
  @toggleTodo
  public toggleComplete (target: HTMLElement, id: number): void {
    
    this.todoData = this.todoData.map((item: ITodoData) => {
      
      if (item.id == id) {
        item.completed = !item.completed
        this.changeComplated(target, item.completed)
      }
      return item
    })
  }
}

export default TodoEvent