# 关于背景图片的一些思考：
#### 1.background-position:
若想要背景图片在盒子的右下角20%处的写法：
background-position: right 20% bottom 20%;

一般超大背景图片的位置为：
background-position: center top;

cover和contain和100%的区别：
cover:缩放背景图片以完全覆盖背景区，可能背景图片部分看不见,（当容器和背景图大小不同时，背景图的 左/右 或者 上/下 部分会被裁剪）
contain:缩放图片完全装入背景区域内，可能背景区的部分空白，（当背景图和容器的大小的不同时，容器的空白区域（上/下或者左/右）会显示由 background-color 设置的背景颜色）
