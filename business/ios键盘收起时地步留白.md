# ios中键盘收起时页面底部区域有留白的问题
问题描述：在输入框输入内容完毕后，点击键盘上的完成按钮时，键盘虽然收起，但是底部却多出来一片大小和键盘高度一样的白色区域，此时如果页面稍微滚动的时候，白色区域就会
消失。所以我们按照这个思路来处理这个问题：
```js
document.body.addEventListener('focusout', ()=> {
    if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
        setTimeOut(()=> {
            const scrollHeight = document.body.scrollTop || document.documentElement.scrollTop
            window.scrollTo(0, Math.max(scrollHeight - 1 ,0))
        },100)
    }
})
```