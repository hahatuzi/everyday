// import * as express from 'express'
const express = require('express')
const {Application} =  require('express')
const { readFileSync } = require('fs')
const { readFile, writeFile, fileOperation } = require('./utils')
// import {Application} from 'express'
// import express, {Application} from 'express'
// import bodyParse from 'body-parser'

const app = express()
console.log('okk');

app.use(express.urlencoded({extended: true}))
app.use(express.json())

app.all('*', (req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-methods', '*')
  next()
})

app.get('/todolist', function (req, res) {
  const todolist = fileOperation('./todo.json')
  res.send(todolist)
  
})

app.post('/toggle', function (req, res) {
  const id = parseInt(req.body.id)
  fileOperation('todo.json', function (todoList) {
    return todoList.map(item => {
      if (item.id == id) {
        item.completed = !item.completed
      }
      return item
    })
  })
  res.send({
    msg:'update ok',
    code:200
  })
})

app.post('/remove', function (req, res) {
  const id = parseInt(req.body.id)

  fileOperation('todo.json', function (todoList) {
    return todoList.filter(item => item.id != id)
  })
  // let todoList = JSON.parse(readFile('todo.json') || '[]')
  // todoList = todoList.filter(item => item.id != id)
  // writeFile('todo.json', todoList)
  res.send({
    msg:'remove ok',
    code:200
  })
})

app.post('/add', function (req, res) {
  const todo = JSON.parse(req.body.todo)
  fileOperation('todo.json', function (todoList) {
    const isExist = todoList.find(item => item.content === todo.content)
    console.log(isExist);
    
    if (isExist) {
      res.send({
        msg: 'isExist',
        code: 200
      })
      return 
    } else {
      todoList.push(todo)
      return todoList
    }
  })
})

app.listen('8080',function () {
  console.log('listening on port 8080');
  
})