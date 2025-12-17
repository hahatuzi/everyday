# excel相关插件
  - 内容解析插件：xlsx
  - 预览插件：vue(@vue-office/excel),react(react-file-viewer)
# xlsx产物转化示意图：
  Blob文件流 --> arrayBuffer --> Read方法读取为book对象（book对象为整个excel文件） -->  提取为对应的sheet对象（sheet对象为excel文件中的单个sheet工作簿） --> 创建workbook --> 输出为excel文件

  ```js
    // excel文件预览
    // https://gitee.com/youlaiorg/vue3-element-admin.git
    <template>
      <div id="excelDom" style="width: 100%; height: 100%; overflow: auto"></div>
    </template>
    
    <script setup>
    import { blobValidate } from "@/utils";
    import service from "@/utils/request";
    import * as XLSX from "xlsx";

    /**
    * 获取xlsx文件
    *
    * @param url xlsx接口地址
    * @param params 接口请求参数
    * @param filename 文件名
    * @param successCallback 文件获取成功的回调函数
    * @param successCallback 文件获取成功的回调函数
    */
    function getFileObjectFromUrl(url, params, filename, successCallback, failCallback) {
      service
        .post(url, params, {
          headers: { "Content-Type": "application/json" },
          responseType: "blob",
        })
        .then((res) => {
          let { data } = res;
          const isBlob = blobValidate(data);
          if (isBlob) {
            const blob = new Blob([data]);
            let file = new File([blob], filename + ".xlsx", { type: blob.type });
            loadExcelAndRender(file, successCallback);
          }
        })
        .catch((r) => {
          console.error(r);
          ElMessage.error("获取数据失败");
          failCallback && failCallback();
        });
     }
    /**
    * 加载xlsx文件
    *
    * @param file 文件内容
    * @param successCallback 文件获取成功的回调函数
    *
    */
    async function loadExcelAndRender(file, successCallback) {
      try {
        const reader = new FileReader();
        reader.onload = function (e) {
          let excelDom = document.getElementById("excelDom");
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          // 获取第一个sheet的名称
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          // 只渲染第一个sheet
          const html = XLSX.utils.sheet_to_html(worksheet, { id: firstSheetName });
          // 将HTML渲染到指定的div中
          excelDom.innerHTML = html;

          // 动态添加细线表格样式
          const table = excelDom.querySelector("table");
          if (table) {
            // 设置表格整体样式
            table.style.borderCollapse = "collapse"; // 合并边框
            table.style.width = "100%"; // 宽度占满容器
            table.style.fontSize = "12px"; // 字体大小
            table.style.lineHeight = "1.5"; // 行高
            table.style.textAlign = "center"; // 文字居中
            table.style.border = "1px solid #e4e7ed"; // 外边框细线

            // 设置表头样式
            const thead = table.querySelector("tr");
            if (thead) {
              thead.style.backgroundColor = "#f2f2f2"; // 表头背景颜色
              thead.style.fontSize = "13px"; // 字体大小
              thead.style.lineHeight = "1.8"; // 行高
              thead.style.fontWeight = "bold"; // 表头字体加粗
              thead.style.whiteSpace = "nowrap"; // 防止内容换行，确保宽度自适应
            }

            // 设置单元格样式
            const cells = table.querySelectorAll("td, th");
            cells.forEach((cell) => {
              cell.style.border = "1px solid #e4e7ed"; // 细线边框
              cell.style.padding = "3px"; // 内边距
              cell.style.minWidth = "70px";
            });
          }
        };
        reader.readAsArrayBuffer(file);
        successCallback();
      } catch (error) {
        console.error("Error loading or rendering Excel:", error);
      }
    }
    defineExpose({
      getFileObjectFromUrl,
    });
    </script>
  ```