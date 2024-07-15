# 1.ref添加类型约束
  ```js
    const count = ref(100) // 会默认进行类型推断
    console.log(count.value)
    const year = ref<number | string>(10) // ref可以通过泛型来添加
    year.value = 'lisa'
  ```
# 2.给reactive添加类型约束，reactive和ref一样可以进行类型推断
  ```js
    type Form = {
      name:string,
      active?:boolean
    }
    const form:Form = reactive({
      name:'lisa'
    })
    // 如果不添加类型约束，form.active会报错
    form.active = false // reactive添加类型约束时，位置和ref不一样，放在变量后面
    // ===================================
    type Address = {
      name:string,
      phone:string,
      gender?:'男' | '女'
    }
    const address:Address = reactive({
      name:'lisa',
      phone:'010-1112',
      gender:'女'
    })
  ```
# 3.给computed标注类型
  ```js
    const count = ref(100)
    const doubleCount = computed(() => {
      return count.value * 2
    }) // 会自动进行类型推断
    // ====================================
    type Goods = {
      id:string,
      name:string,
      age:number
    }
    const goods = ref<Goods[]>([])
    goods.value = [
      {id:'100',name:"lisa",age:18},
      {id:'101',name:"jisoo",age:20},
    ]
    const newGoods = computed(() => {
      return goodList.value.filter(item => item.age > 18)
    })
  ```
# 4.给事件处理函数添加类型约束
  ```js
    const inputChange = (e:Event) => {
      // 当change时间触发的时候，获取文本框中的数据
      console.log((e.target as HTMLInputElement).value)
    }
    const handleClick = (e:Event) => {
      console.log((e.target as HTMLButtonElement).innerHTML)
    }
    <button @click="handleClick"></button>
  ```
# 5.给模板引用ref添加
  ```js
    const inputRef = ref<HTMLInputElement | null>(null)
    onMounted(() => {
      inputRef.value?.focus() // 页面加载完毕后input框获取焦点,添加可选链，防止报错
      console.log(aRef.value?.href)
    })
    {/* // ======================== */}
    const aRef = ref<HTMLAnchorElement | null>(null)
    <a href="baidu.com" ref="aRef"></a>
    <input type="text" @change="inputChange" ref="inputRef">
  ```
# 6.给自定义组件添加类型约束:instanceType<typeof 组件名>
  ```js
    import MyModal from './component/MyModal.vue'
    const modal = ref<instanceType<typeof MyModal> | null>(null)
    const handleCLick = () => {
      modal.value?.open()
    }
    <MyModal ref="modal"></MyModal>
  ```
# 7.对象的空值处理
  ```js
    // 使用可选链
    inputRef?.value.focus()
    // 非空断言！
    inputRef!.value
  ```
# 8.给defineProps添加类型注解和默认值
  ```js
    interface Props {
      color:string,
      size?:string
    }
    const props = withDefaults(defineProps<Props>(),{
      size:'small'
    })
    // ======================================================
    defineProps<{ msg: string }>()
    <h1>{{ msg }}</h1>
  ```
# 9.给emits添加类型注解，通过defineEmits<Emits>()泛型传参
```js
    // 实现emit('get-msg',msg:string)
// 定义事件类型Emits
type Emits = {
  (e:'get-msg',msg:string):void
}
 const emit = defineEmits<Emits>()
 emit('get-msg', '传递给父组件消息')
 // ===================================

```
# 10.类型声明文件
  - 比较老的第三方包：比如jquery,从DefinitelyTyped库中下载第三方包的类型声明文件
  - 前后端交互时：自定义类型声明文件,使用axios.request<ResData>({})
# 定时器
```js
let timer: NodeJS.Timer | null = null;
timer = setInterval(() => {
  let str = new Date();
  time.second =
    str.getSeconds() < 10 ? "0" + str.getSeconds() : "" + str.getSeconds();
}, 1000);
  clearInterval(timer as unknown as number);
```
# 11.声明iframe的contentwindow
# 12.vue-router的类型约束：RouteRecordRaw
```js
export const constantRoutes:RouteRecordRaw[] = []
```
# 13.路由内置对象：RouteRecordRaw
```js
export const constantRoutes: RouteRecordRaw[] = [
  {}
]
```
# 14.axios使用
```js
export interface Http {
  request<T>(method:string,url:string,params?:unknown):Promise<T>
}

onMounted(async() => {
  let res = await http.request<{data:TableData[],total:number}>()
})
```