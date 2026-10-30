
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
  ### (2)router.navigate,路由跳转
  ```js
    import {userRouter} from 'expo-router'
    const router = useRouter
    // 方式一：
    <TouchableOpacity onPress={router.navigate('/details')}>
      <Text>跳转{navigate}</Text>
    </TouchableOpacity>
    // 方式二：
    <TouchableOpacity onPress={()=>router.navigate({pathname:'/course/[id]',params:{id:4})}></TouchableOpacity>
  ``` 
  ### (3)router.replace，路由替换
  ### (4)router.push
  ### (5)动态路由与参数跳传递方式
  ```js
    // 在app文件夹下新建app/courses/[id].js文件
    // 方式一：
    <Link href="{{pathname:'/courses/[id]',params:{id:2}}}">
    // 方式二：
    <TouchableOpacity onPress={()=>router.navigate({pathname:'/course/[id]',params:{id:4})}></TouchableOpacity>
  ```

## Stack页面栈,管理页面路由堆栈
```js
  import {Stack  } from "expo-router";

  export default function Layout () {
    return <Stack
      screenOptions={{
        headerTitleAlign:'center', // 安卓标题栏居中
        animation:"slide_from_right", // 安卓使用左右切屏
        headerStyle:{ // 导航栏的整体样式
          backgroundColor:'#e29447',
        },
        headerTintColor:'#fff', // 导航栏中文字，按钮，图标的颜色
        headerTitleStyle:{ // 导航栏标题样式
          fontSize:16,
        },
        headerBackButtonDisplayMode:"minimal"
      }}
    >
      {/* Tabs */}
      <Stack.Screen name="(tabs)" options={{headerShown:false}}></Stack.Screen>
      {/* Cards */}
      <Stack.Screen name="articles/index" options={{title: '通知'}}></Stack.Screen>
      <Stack.Screen name="setting/index" options={{title: '设置'}}></Stack.Screen>
      <Stack.Screen name="courses/[id]" options={{title: '课程详情'}}></Stack.Screen>
      <Stack.Screen name="search/index" options={{title: '搜索'}}></Stack.Screen>
      <Stack.Screen name="teachers/[id]" options={{title: '教师详情',presentation:"modal"}}></Stack.Screen>
    </Stack>

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
## 导航栏Stack.Screen
> _layout.js中的Stack标签的options是各个页面都通用的样式
  ```js
    // _layout.js中的写法
    <Stack
      screenOptions={{
        headerTitleAlign:'center', // 安卓标题栏居中
        animation:"slide_from_right", // 安卓使用左右切屏
        headerStyle:{ // 导航栏的整体样式
          backgroundColor:'#e29447',
        },
        headerTintColor:'#fff', // 导航栏中文字，按钮，图标的颜色
        headerTitleStyle:{ // 导航栏标题样式
          fontWeight:'bold'
        }
      }}
    />
    // 各页面单独的写法
    <Stack.Screen options={{
      title:'首页',
      headerStyle:{ // 导航栏的整体样式
        backgroundColor:'#e29447',
      },
      headerTintColor:'#fff', // 导航栏中文字，按钮，图标的颜色
      headerTitleStyle:{ // 导航栏标题样式
        fontWeight:'bold'
      },
      headerTitle: props => <LogoTitle {...props}></LogoTitle>,
      headerLeft:() => <HeaderButton name="bell" href="/articles" style={styles.headerLeft}></HeaderButton>,
      headerRight:()=> <>
        <HeaderButton name="magnifier" href="/search" style={styles.headerRight}></HeaderButton>
        <HeaderButton name="options" href="/setting" style={styles.headerRight}></HeaderButton>
      </>
    }}>
    <Stack.Screen name="courses/[id]" options={({route}) => ({title:route.params?.title || '课程页'})}></Stack.Screen>
    </Stack.Screen>
  ```

## tabbar标准配置
> 在app文件夹下新建app/(tabs)/_layout.js文件，index.js文件，videos.js文件，user.js文件
  ```js
    function HeaderButton (props) {
      const {name, ...rest} = props
      return (
        <Link asChild {...rest}>
          <TouchableOpacity>
            <SimpleLineIcons size={16} color="#1f99b0" name={name}></SimpleLineIcons>
          </TouchableOpacity>
        </Link>
      )
    }
    function TabBarIcon (props) {
      return <SimpleLineIcons size={25} {...props}></SimpleLineIcons>
    }
    export default function TabLayout () {
      return (
        <Tabs screenOptions={{
          headerTitle: props => <LogoTitle {...props}></LogoTitle>,
          headerTitleAlign:"center",
          headerLeft:() => <HeaderButton name="bell" href="/articles" style={styles.headerLeft}></HeaderButton>,
          headerRight:()=> <>
            <HeaderButton name="magnifier" href="/search" style={styles.headerRight}></HeaderButton>
            <HeaderButton name="options" href="/setting" style={styles.headerRight}></HeaderButton>
          </>,
          tabBarActiveTintColor:'#1f99b0',  // 当前选中的tabbar的图标颜色
          // 取消tabbar切换时的android的水波纹效果
          tabBarButton: (props) => (
            <TouchableOpacity {...props} activeOpacity={1} style={[props.style, {backgroundColor:'transparent'}]}></TouchableOpacity>
          )
        }}>
        // tabBarIcon，tabbar的icon
          <Tabs.Screen name="index" options={{title:'发现',tabBarIcon:({color})=> <TabBarIcon name="compass" color={color}></TabBarIcon>}}></Tabs.Screen>
          <Tabs.Screen name="videos" options={{title:'视频',tabBarIcon:({color})=> <TabBarIcon name="camrecorder" color={color}></TabBarIcon>}}></Tabs.Screen>
          <Tabs.Screen name="user" options={{title:'我的',tabBarIcon:({color})=> <TabBarIcon name="user" color={color}></TabBarIcon>}}></Tabs.Screen>
        </Tabs>
      )
    }
  ```
## Model模态页
## src的别名@
  ```js
    npx expo customize babel.config.js
    npm i babel-plugin-module-resolver
    修改babel.config.js文件内容为以下内容：
    module.exports = function (api) {
      api.cache(true)
      return {
        presets:['bebel-preset-expo'],
        plugins:[
          [
            'module-resolver',
            {
              root:['./src'],
              alias:{
                '@':'./src'
              }
            }
          ]
        ]
      }
    }
    npx expo start --clear
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
  
## ios液态玻璃NativeTabs
  - diableTransparentOnScrollEdge,防止ios18以下机型的NativeTabs在FlagList中变透明
  ```js
    <NativeTabs>
        <NativeTabs.Trigger name="index">
          <Label></Label>
          <Icon></Icon>
        </NativeTabs.Trigger>   
    </NativeTabs>
  ```