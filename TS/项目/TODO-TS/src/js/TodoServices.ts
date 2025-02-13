import $ from 'jquery'
import { ITodoData } from './typings';

export function getTodoList (
  target: any,
  methodName:string,
  descriptor: PropertyDescriptor
) {
  const _origin = descriptor.value

  descriptor.value = function (todoData: ITodoData) {
    $.get('http://localhost:8080/todolist').then((res:string) => {
      
      if (!res) return
      todoData = JSON.parse(res)
    }).then(() => {
      // _origin(todoData)
      _origin.call(this, todoData)
    })
  }
}

export function removeTodo (
  target: any,
  methodName:string,
  descriptor: PropertyDescriptor
) {
  const _origin = descriptor.value

  descriptor.value = function (target:HTMLElement, id:number) {
    $.post('http://localhost:8080/remove', { id }).then((res:string) => {
      console.log(res, 'remove');
      _origin.call(this, target)
    })
  }
}

export function toggleTodo (
  target: any,
  methodName:string,
  descriptor: PropertyDescriptor
) {
  const _origin = descriptor.value
  descriptor.value = function (target:HTMLElement, id:number) {
    $.post('http://localhost:8080/toggle', { id }).then((res:string) => {
      _origin.call(this, target, id)
    })
  }
}

export function addTodo (
  target: any,
  methodName:string,
  descriptor: PropertyDescriptor
) {
  const _origin = descriptor.value
  descriptor.value = function (todo: ITodoData) {
    $.post('http://localhost:8080/add', {todo: JSON.stringify(todo)}).then((res:string) => {
      console.log(res);
      
      // if (res.msg == 'isExist') {
      //   return
      // }
      _origin.call(this, todo)
    })
  }
}