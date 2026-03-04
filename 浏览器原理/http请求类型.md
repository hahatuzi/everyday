# MIME类型,是一种标准用来表示文件或者数据的格式，广泛应用于http协议，文件上传下载，API数据传输等
**MIME类型通常由主类型type和子类型subType组成：type/subType**
|    主类型   |               描述              |                   示例                |
| ----------- | --------------------------------| --------------------------------------|
|     text    |             文本类型            |            text/plain,text/html       |
|    image    |              图片类型           |        image/png,image/jpeg           |
|    audio    |              音频类型           |        audio/mpeg,audio/wav           |
|     video   |                 视频            |     video/mp4,video/webm              |
| application |  应用程序数据(比如二进制文件)   |    application/xml,application/json   |
|  multipart  |     多部分数据(比如邮件附件)    |    multipart/form-data                |

# 二：MIME类型应用场景
  - http请求时content-type:application/json
  - http响应时：accept
  - html文件引入：<link type="text/css">