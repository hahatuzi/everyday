# 列表渲染
#### 1.wx:key
(1)wx:key="item的一个属性名"
(2)wx:key="*this",代表for兴顺的item本身，此方式需要item本身是一个唯一的字符串或者数字
##### 2.wx:for-item
可以指定数组当前元素的变量名：例如：wx:for-item="itemName"
##### 3.wx:for-index
可以指定数组当前下标的变量名:例如：wx:for-index="idx"
# wx:if和hidden对组件的生命周期的影响
在了解这两个语法对组建带来的影响之前我们先列举一下页面和自定义组件的生命周期
#### 1.页面：init(视图层) ---> onload(逻辑层) ---> onShow(逻辑层)  --传递数据给视图层--> first Render Ready (视图层) ---> onReady(逻辑层) ---传递数据给视图层---> rerender
--->  onHide  ------>  onShow  ---> onUnload
#### 2.自定义组件：
**（1）lifetimes**
created:组件刚被创建好，此时，**this.data就是在Component中定义的data，还不能调用setData**
attached:此时组件已经进入页面节点树，此时完成绝大部分操作
ready:组件在视图层布局完成
moved:组件被转移到页面节点树的另外一个地方
detached：组件离开页面节点树
error:组件方法抛出错误
**（1）pagelifetimes**
show:组件所在的页面被展示
hide:组件所在的页面被隐藏
resize:组件所在页面尺寸改变
#### 对比：
当一个页面中含有多个wx:if,wx:else的组件时，第一次仅会展示wx:if=“true”的组件，即仅会经历它的生命周期(created,attached,ready)
当多个组件之间用hidden来切换时，第一次进入页面就会经历所有组件的所有生命周期(created,attached,ready)，且切换时不再触发生命周期
wx:if(created,attached,ready)
# <wxs>标签的解析
# 小程序组件的npm发布
# 小程序全局样式和局部样式
app.wxss中为全局样式，局部页面样式page.wxss仅对当前页面生效