# 1.y轴保留小数点后几位
```js
  yAxis: {
    axisLabel:{
      formatter:function(value,index){
          return value.toFixed(2) //保留两位小数
      }
    }
  },
```
# 2.鼠标悬停时的轴线颜色
```js
  tooltip: {
    axisPointer:{
      type: 'line',
      lineStyle:{
        color: '#000'
      }
    }
  }
```
# 3.ecahrts数据为空时的空状态展位
[!参考链接]https://blog.csdn.net/qq_43586648/article/details/118363037?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-118363037-blog-122069466.pc_relevant_recovery_v2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-118363037-blog-122069466.pc_relevant_recovery_v2
```js
// 使用一个预先定义的option占位
  var option = {
    title: {
        text: ' {a|}',
        x: 'center',
        y: 'center',
        subtext,
        itemGap: -20,
        textStyle: {
            rich: {
              a: {
                color: '#000',
                fontSize: '16',
                height: 80,
                width: 160,
                backgroundColor: {
                  image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNDEiIHZpZXdCb3g9IjAgMCA2NCA0MSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4NCiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCAxKSIgZmlsbD0ibm9uZSIgZmlsbFJ1bGU9ImV2ZW5vZGQiPg0KICAgIDxlbGxpcHNlIGZpbGw9IiNkZGQiIGN4PSIzMiIgY3k9IjMzIiByeD0iMzIiIHJ5PSI3IiAvPg0KICAgIDxnIGZpbGxSdWxlPSJub256ZXJvIiBzdHJva2U9IiM5OTkiPg0KICAgICAgPHBhdGgNCiAgICAgICAgZD0iTTU1IDEyLjc2TDQ0Ljg1NCAxLjI1OEM0NC4zNjcuNDc0IDQzLjY1NiAwIDQyLjkwNyAwSDIxLjA5M2MtLjc0OSAwLTEuNDYuNDc0LTEuOTQ3IDEuMjU3TDkgMTIuNzYxVjIyaDQ2di05LjI0eiIgLz4NCiAgICAgIDxwYXRoDQogICAgICAgIGQ9Ik00MS42MTMgMTUuOTMxYzAtMS42MDUuOTk0LTIuOTMgMi4yMjctMi45MzFINTV2MTguMTM3QzU1IDMzLjI2IDUzLjY4IDM1IDUyLjA1IDM1aC00MC4xQzEwLjMyIDM1IDkgMzMuMjU5IDkgMzEuMTM3VjEzaDExLjE2YzEuMjMzIDAgMi4yMjcgMS4zMjMgMi4yMjcgMi45Mjh2LjAyMmMwIDEuNjA1IDEuMDA1IDIuOTAxIDIuMjM3IDIuOTAxaDE0Ljc1MmMxLjIzMiAwIDIuMjM3LTEuMzA4IDIuMjM3LTIuOTEzdi0uMDA3eiINCiAgICAgICAgZmlsbD0iI2UxZTFlMSIgLz4NCiAgICA8L2c+DQogIDwvZz4NCjwvc3ZnPg==',
                }
              },
            }
        },
        subtextStyle: {
          fontSize: 16,
        }
    }
  }
```