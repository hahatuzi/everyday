[!https://cloud.tencent.com/developer/article/2325229]复盘大厂常问的项目难点

# 1.页面截图功能实现,包括iframe时！！！
```js

  <div class="construct_container" id="img_canvas" v-if="!making">
    <div class="map" id="map_canvas">
      <iframe id="i_map" style="width:100%; height:100%;"  scrolling="no"></iframe>
    </div>
  </div>

  // 制图
  function makeImg () {
    making.value = true
    // 将iframe内容转化为图片
    let iframe=document.getElementById("i_map")
    let iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    let canvas = iframeDoc.getElementsByTagName('canvas')[0];
    let dataURL = canvas.toDataURL('image/png');
    let img = document.createElement('img')
    img.src = dataURL;
    // 创建新的地图容器，并添加转化后的地图图片
    let cloneMapDom = document.createElement('div')
    cloneMapDom.id = 'map_canvas'
    cloneMapDom.appendChild(img)

    // 克隆总元素
    let dom = document.getElementById('img_canvas')
    let cloneDom = dom.cloneNode(true)
    // 将新创建的地图容器添加至克隆后的总元素中
    cloneDom.removeChild(cloneDom.firstChild)
    cloneDom.appendChild(cloneMapDom)
    // 作为临时元素挂载
    document.body.appendChild(cloneDom)
    html2canvas(cloneDom).then(canvas => {
      let img = canvas.toDataURL('image/png')
      fileDownload(img)
      // 导出完毕后删除克隆元素
      document.body.removeChild(cloneDom)
      making.value = false
    }).catch(error => {
      console.error(error)
    })
  }
  // 下载图片方法
  const fileDownload = (downloadUrl) => {
    let aLink = document.createElement("a");
    aLink.style.display = "none";
    // 以防base64过长导致下载失败，所以将base64转成blob格式
    aLink.href = URL.createObjectURL(dataURIToBlob(downloadUrl));
    aLink.download = "img.png";
    document.body.appendChild(aLink);
    aLink.click();
    document.body.removeChild(aLink);
  };

   // base64转blob方法
  const dataURIToBlob = (dataURI) => {
    let binStr = atob(dataURI.split(",")[1]),
      len = binStr.length,
    arr = new Uint8Array(len);
      
    for (var i = 0; i < len; i++) {
      arr[i] = binStr.charCodeAt(i);
    }
    return new Blob([arr]);
  };
```