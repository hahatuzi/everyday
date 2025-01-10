# http相关知识
  ### content-Type
  - application/x-www-form-urlencoded;charset=utf-8  -->  name=lisa&age=18
  - application/json;charset=utf-8 -->  {name:'lisa', age: 18}
  - multipart/form-data

# json-server:快速搭建一个restful接口请求
  - 第一步：npm install -g json-server
  - 第二步： 创建db.json添加mock数据
  ```js
    {
      "posts": [
        {
          "id": 1,
          "title": "json-server",
          "author": "typicode"
        },
        {
          "id": 2
        },
        {
          "name": "lisa",
          "id": 3
        },
        {
          "name": "lisa",
          "id": 4
        },
        {
          "name": "lisa",
          "id": 5
        }
      ],
      "comments": [
        {
          "id": 1,
          "body": "some comment",
          "postId": 1
        }
      ],
      "product1": [
        {
          "id": 1,
          "body": "some comment",
          "postId": 1
        }
      ],
      "product2": [
        {
          "id": 1,
          "body": "some comment",
          "postId": 1
        }
      ],
      "profile": {
        "name": "typicode"
      }
    }
  ```
  - 第三步：运行命令json-server --watch db.json,得到可访问的接口http://localhost:3000/posts，http://localhost:3000/comments