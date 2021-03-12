# 问题：同一个元素不能同时应用transform属性和animate属性
# 解决：将其中一个属性应用至父级元素
# 实例：
```js
<div>
  <img src="">
</div>
div{
    position:absolute;
    left:50%;
    transfrom:translate(-50%);
    // 可将transform和animate其中一个属性应用至父级元素上
    img{
        animate:breathe 2s infinite;
    }
}
@keyframe breathe{
    0%{
        transform:scale(1);
    }
    50%{
        transform:scale(0.8);
    }
    100%{
        transform:scale(1);
    }
}
```