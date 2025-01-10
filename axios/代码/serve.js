const express = require('express')
const cors = require('cors')
const app = express()
app.use(cors())
app.use(express.urlencoded())
app.use(express.json())
app.get('/product1',(req,res)=>{

  setTimeout(() => {
    
    if (!res.headersSent) {
      res.send([{id:1}])
    }
  }, 10000);
})
app.get('/product2',(req,res)=>{
  setTimeout(() => {
    res.send([{id:2}])
  }, 5 * 1000);
})
app.get('/profile',)
app.listen(3000,()=>{
  console.log('server start')
})