# CSS控制图片HTTP请求的情形实例解析：
一：作为img标签
（1）：display：none属性控制，除opera外均会发生请求
（2）：visibility:hidden，均产生请求
（3）：
二：作为背景图片
（1）挂靠元素存在时：发生请求
    display:none，Opera和Firefox对于用display: none隐藏的元素背景，不会产生HTTP请求
    visibility:hidden
    多重背景图时：CSS写法时：只会请求最后一次，前面的都会被覆盖
    ```js
    <style>
    .test{
        background:url('1')
    }
    .test{
        background:url('2')
    }
    </style>
    <div class="test"></div>
    ```
    CSS3写法时：webkit引擎会都请求，因为支持c3写法
    ```js
    <style>
    .test{
        background-image:url('1'),url('2')
    }
    </style>
    <div class="test"></div>
    ```
（2）挂靠元素不存在时：不发生请求