
## 安装与使用
  ### Expo安装
  Xcode, Expo go,
  ### Expo启动react native项目
  - npx create-expo-app@latest --template blank
  - 启动android studios的虚拟设备
  - adb devices
  - npx expo start
  - a
  ### Expo的命令
  ```js
    # ---------- Expo ----------
    npx create-expo-app@latest MyApp
    cd MyApp && npx expo start          # 扫码运行
    npx expo prebuild                   # 生成 ios/ android/（CNG）
    npx expo run:ios / run:android      # 本地原生构建
    eas build --platform all            # 云端构建
    eas update --branch production      # OTA 热更新
    adb devices #查看andriod studio启动的设备

  ```
## Expo Router
  > React Navigation相较于ExpoRouter来说使用困难
  ### 使用方式：
  - npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-contants expo-status-bar
  - 修改package.json的main为expo-router/entry
## 路由跳转页面
  ### (1)Link组件
  ```js
    <Link href="../">返回</Link>
    <link href="/details">跳转到详情页</Link>
  ```
  ### (2)router.navigate
  ```js
    import {userRouter} from 'expo-router'
    const router = useRouter
    <TouchableOpacity onPress={router.navigate('/details')}>
      <Text>跳转{navigate}</Text>
    </TouchableOpacity>
  ```
  ### (3)router.replace
  ### (4)router.push
  ### (5)路由跳转传参方式
  ```js
    <Link href="{{pathname:'/course/[id]',params:{id:2}}}">
    <TouchableOpacity onPress={()=>router.navigate({pathname:'/course/[id]',params:{id:4})}></TouchableOpacity>
  ```

## Stack页面栈
```js
export default function Layout () {
  return <Stack></Stack>
}
```
## Slot插槽
```js
  
```
## 使用自定义组件配置导航栏
  ```js
    function HeaderLeft () {
      return (
        <Link>返回</Link>
      )
    }
    function HeaderButton (props) {
      const {name, ...rest} = props
      return (
        <Link aasChild={...rest}>
          <TouchableOpacity>
            <SimpleLineIncons size={20} color="#1f99b0" name={name}></SimpleLineIncons>
          </TouchableOpacity>
        </Link>
      )
    }
    <Stack.Screen
      name="index"
      options={{
        headerTitle: props => <LogoTtitle {...props}></LogoTtitle>,
        headerLeft:()=> <HeaderButton name="bell" href="/articles"></HeaderButton>,
        headerRight:()=><HeaderRight></HeaderRight>
      }}
    >    
    </Stack.Screen>00000 
  ```
## tabbar标准配置 
  ```js
    
  ```
## src的别名@
  ```js
    npx expo customize babel.config.js
    npm i bable-plugin-module-resolver
    npx expo start clear
    - 新建jsconfig.json
    {
      "compilerOptions":{
        "baseUrl":".",
        "paths":{
          "@/*":["./src/*"]
        }
      },
      "exclude":["node_modules","**/node_modules/*"]
    }
  ```
## 更新expo SDK以及依赖包
  - npm i expo@latest
  - npx expo install --fix