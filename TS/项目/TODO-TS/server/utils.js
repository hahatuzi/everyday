const { readFileSync, writeFileSync } = require('fs')
const {resolve} = require('path')

function readFile (path) {
  return readFileSync(resolve(__dirname, path), 'utf-8')
}

function writeFile (path, data) {
  return writeFileSync(resolve(__dirname, path), JSON.stringify(data))
}

function fileOperation (path, fn) {
  let todoList = JSON.parse(readFile('todo.json') || '[]')
  if (!fn) {
    return JSON.stringify(todoList)
  }

  todoList = fn(todoList)
  writeFile(path, todoList)
}
module.exports = {
  readFile,
  writeFile,
  fileOperation
}