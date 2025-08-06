# flex:1和flex:auto的区别
```js
// flex-grow:项目的增长系数，项目在剩余空间的相对比例：默认为0，即如果存在剩余区域，该项目不会放大。
// flex-shrink:项目的缩收缩规则：默认为1，即如果可分配空间不足，会适当缩小项目。flex元素仅在默认宽度之和大于容器的时候才会收缩
// flex-basis:在分配空间之前，项目的主轴空间，相当于我们设置的width
flex:none: // flex: 0 0 auto;表示项目不会伸缩，保持原始大小
flex:1:  // flex: 1 1 0%;
flex:auto: // flex: 1 1 auto;表示项目会根据自身大小和剩余空间进行缩放
// 如果width和flex-basis同时设置，非auto的flex-basis权重更大
<div class="flex-box">
    <div class="item1">短文本</div>
    <div class="item2">文本内容一定要比item长，文本内容一定要比item长</div>
</div>

<style type="text/css">
    .flex-box{
         display: flex;
         width: 1000px;
         text-algin:center;
    }

    .item1 {
        height: 100px;
        flex: 1 1 0%; /*flex-basis为0%，覆盖width，实际占用0*/
        background:red;
    }

    .item2 {
        height: 100px;
        width: 400px;
        flex: 1 1 auto;  /*flex-basis为auto，width权限更高，占用300*/
        background:green;
    }
    /* 分配宽度前：
    字元素占用空间为：0+400
    可分配空间：600
    放大比例：1:1，获取的可放大空间：300+300
    */
    /* 实际子元素空间：
    0+300
    400+300
    */
</style>
```