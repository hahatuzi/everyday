import {ITodoData} from './js/typings';
import TodoEvent from './js/TodoEvent';

;((doc) => {
  const oInput:HTMLInputElement = document.querySelector('input')
  const oAddBtn:HTMLElement = document.querySelector('button')
  const oTodoList:HTMLElement = document.querySelector('.todo-list')

  const todoData: ITodoData[] = [
    // {id: 1, content: '1', completed: true},
    // {id: 2, content: '12', completed: true},
    // {id: 3, content: '123', completed: true},
    // {id: 4, content: '1234', completed: true},
    // {id: 5, content: '12345', completed: true},
  ]

  const todoEvent: TodoEvent = new TodoEvent(todoData, oTodoList)
  const init = ():void => {
    bindEvent()
  }

  function bindEvent():void {
    oAddBtn.addEventListener('click', handleAddBtnClick, false)
    oTodoList.addEventListener('click', handleListClick, false)
  }

  function handleAddBtnClick ():void {
    const val: string = oInput.value.trim()
    
    if (val.length) {
      const res = todoEvent.addTodo(<ITodoData>{
        id: new Date().getTime(),
        content: val,
        completed:false
      })
      console.log(res);
      
      if (res && res === 1001) {
        alert('该列表项已经存在')
      }
      console.log(todoData);
    }
    
  }
  
  function handleListClick (e:MouseEvent):void {
    const target = e.target as HTMLElement
    const tagName = target.tagName.toLowerCase()
    console.log(tagName);
    
    if (tagName === 'input' || tagName === 'button') {
      const id = parseInt(target.dataset.id)
      switch (tagName) {
        case 'input':
          todoEvent.toggleComplete(target, id)
          break;
        case 'button':
          todoEvent.removeTodo(target, id)
          break;
        default:
          break;
      }
    }
  }

  init()
})(document)