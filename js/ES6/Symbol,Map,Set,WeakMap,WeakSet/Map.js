const obj1 = {name:'lisa'}
    const obj2 = {name:'lili'}
    const info = {
      [obj1]: 'a',
      [obj2]:'b'
    }
    console.log(info) // { '[object Object]': 'b' }
    const map = new Map()
    map.set(obj1, 'a')
    map.set(obj2, 'b')
    console.log(map) // { { name: 'lisa' } => 'a', { name: 'lili' } => 'b' }