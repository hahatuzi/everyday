## 目录

- [目录](#目录)
- [一、总结](#一总结)
- [二、对比](#二对比)
- [三、Expo短板](#三expo短板)
- [四、ReactNativeCLI优势](#四reactnativecli优势)
- [五、ReactNativeCLI短板](#五reactnativecli短板)

---
## 一、总结
> **Expo 是一套封装好的上层开发框架 + 工具链（基于 RN）；React Native CLI 是原生 RN 底层脚手架，直接管理 ios/android 原生工程**。
> 现在 Expo 分两种工作流：**Managed（托管）、Dev Build / Prebuild（裸工作流，不再叫 eject）**
---
## 二、对比
  | **对比维度** | **Expo（Managed 托管）** | **Expo（Dev Build / Prebuild）** | **React Native CLI** |
  |------------|------|------|------|
  |原生工程文件|                无 ios/android 文件夹                 | expo prebuild 自动生成，可通过 config plugin 扩展 | 手动维护 ios/android，提交到 git |
  |  初始化环境|    只需 Node，**不需要 Xcode、Android Studio**       | Node，构建时依赖原生环境 / EAS 云构建 | 必须安装 Xcode、Android Studio、JDK、SDK，环境配置繁琐 |
  |   开发调试 |            Expo Go App 扫码预览，开箱即用            | 自己打自定义开发客户端，支持带原生模块 | 模拟器 / 真机 |
  |原生模块限制|    只能使用 Expo SDK 兼容库，不支持自定义原生代码    | 支持绝大多数原生模块、自定义原生代码，用 config plugin 配置 | 全部原生库都支持，可手写 Swift/Kotlin 原生代码|
  | OTA 热更新 |                  内置 EAS Update，开箱即用           | EAS Update 支持 | 无内置，需要 CodePush 等第三方方案 |
  |  构建打包  |            EAS Build 云端打包，不用 Mac 打 iOS       | EAS Build / 本地打包 |本地打包，iOS 打包必须 Mac，证书、签名全手动管理 |
  |    路由    |      内置 Expo Router 文件路由                       | Expo Router    | 需要自己集成 React Navigation |
  |   Web 支持 |                一等公民，一套代码跑 Web              | 支持 | 需要手动配置 react-native-web |
  | RN 版本升级| 跟随 Expo SDK 版本，固定绑定RN 版本，升级 SDK 大版本 | 同样跟随 SDK | 可自由升级 RN 版本，但是原生工程改动多，升级坑多 |
  |   包体积   |                            基础包偏大                | 比托管略小 | 基础包最小，可控性最强 |
  |   学习门槛 |                   低，前端开发者直接上手             | 中等，需要了解 config plugin | 高，团队最好有 iOS/Android 原生开发 |
  |   适用场景 |          MVP、Demo、普通业务 App、快速迭代           | 业务 App + 需要少量原生 SDK、支付、蓝牙等 | 深度原生定制、现有原生 App 嵌入 RN（Brownfield）、硬件 SDK、复杂底层能力 |

---
## 三、Expo短板

1. **托管模式有库黑名单**：很多重度原生库（自研 SDK、特殊蓝牙、Android 后台服务、音视频底层）无法直接在 Expo Go 运行，需要切 Dev Build
2. **RN 版本滞后**：不能第一时间用上 React Native 最新版本，要等 Expo SDK 适配
3. **EAS 高级服务有成本**：免费额度有限，大规模持续构建需要付费
4. **抽象层**：原生层能力被封装，底层调优、深度定制不如裸 RN CLI 灵活
---

## 四、ReactNativeCLI优势

1. **完全控制权**：直接修改 Xcode 工程、Android Gradle、原生代码，没有中间层限制，任何原生 SDK、硬件能力都能接入
2. **Brownfield（混编）首选**：把 RN 页面嵌入现有 iOS/Android 原生项目，这个场景 Expo 托管天然不适合
3. **包体积、性能精细调优**：可以手动裁剪、原生侧优化，极限性能场景更可控
4. **RN 版本自主**：可以按需升级 RN，不受 Expo SDK 节奏约束

---
## 五、ReactNativeCLI短板

1. **环境地狱**：新人配置环境极其痛苦，pod、gradle、JDK 版本冲突是高频问题
2. **升级噩梦**：RN 大版本升级，大量原生文件改动，经常需要手动修复 ios/android 工程
3. **能力都是裸的**：路由、热更新、推送、文件、图片都要自己集成、配置
4. **打包麻烦**：iOS 打包必须 Mac，证书、描述文件、签名全手动维护，CI 搭建成本高
---