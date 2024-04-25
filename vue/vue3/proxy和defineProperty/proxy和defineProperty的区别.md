# proxy和Object.defineProperty的比较

### 1.可以监视到风多的对象操作，比如delete操作和对象中方法的调用
  ```js
    const person = {
      name:'lisa',
      age:18
    }
    const proxy_person = new Proxy(person,{
      deleteProperty(target, prop){
        console.log('delete')
        delete target[prop]
      }
    })
    delete proxy_person.age
    console.log(proxy_person)
  ```

### 2.proxy支持对数组的操作
  ```js
    let arr = []
    let proxy_arr = new Proxy(arr,{
      set(target, prop, value) {
        target[prop] = value
        // const isOK = Reflect.set(target,prop,value)
        // return isOK
        return true
      }
    })
    proxy_arr.push(1)
    console.log(proxy_arr)
    console.log(arr)
  ```
### 3.不需要侵入对象就可以对它的内部进行读写
  ```js
    const person ={}
    const personProxy = new Proxy(person,{
        get(target ,property){
            return target[property]
            // return Reflect.get(target,prop)
        },
        set(target,property,value){
            target[property] = value
        // const isOK = Reflect.set(target,prop,value)
        // return isOK
        return true
        }
    })
    // ================Object.defineProperty=========================
    const obj = {}
    Object.defineProperty(obj, 'name',{
      get(){
        return obj.__name
      },
      set(value){
        obj.__name = value
      }
    })
    obj.name = 'lisa'
  ```

### 附录.proxy的handler方法列表
|              handler               |                   调用方式                 |
| ---------------------------------- | -------------------------------------------|
|                  get               |                   读取属性                 |
|                  set               |                   新增属性                 |
|                  has               |                   in操作符                 |
|                 apply              |                 调用一个函数               |
|               cnostruct            |                      new                   |
|           defineProperty           |          Object.defineProperty             |
|           deleteProperty           |               delete操作符                 |
|              getProperty           |          Object.getPropertyOf              |
|              setProperty           |          Object.setPropertyOf              |
|              isExtensible          |           Object.isExtensible              |
|          preventExtensions         |        Object.preventExtensions            |
|      getOwnPropertyDescriptor      |       Object.getOwnPropertyDescriptor      |
|                ownKeys             |  Object.keys( ) \ Object.getOwnPropertyNames( ) \ Object.getOwnPropertySymbols( )  |