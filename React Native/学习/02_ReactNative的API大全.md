## 目录

- [目录](#目录)
- [一、style样式](#一、style样式)
- [二、对比](#二对比)
- [三、Expo短板](#三expo短板)
- [四、ReactNativeCLI优势](#四reactnativecli优势)
- [五、ReactNativeCLI短板](#五reactnativecli短板)

---
## 一、style样式
  ```js
  // 数组类型
  import {StyleSheet, Text, View} from 'react-native'
  <view style={[{fontSize:50},styles.title]}></view>
  const styles = StyleSheet.create({
    title:{
      fontSize:20,
      fontWeight:'bold'
    })
  ```
## 二、FlexBox布局
## 三、核心组件
  ### 3.1 View
  ### 3.2 Text
  - numberOfLines:文本超出一行时，用几行来显示它
  ### 3.3 Image
  > expo的Image组件和ReactNative的Image组件的区别：Expo功能更多
  ### 3.4 Button和Alert
  - onPress
  - alert
  - prompt(ios)
    ```js
      static alert (
        title: string,
        message?: string,
        buttons?: AlertButton[],
        options?: AlertOptions,
      );
      const onPressed = () => {
        Alert.alert('提示信息','请问确定删除以下数据吗',[
          {text:"取消",onPress:() => console.log('取消了')},
          {text:"确定",onPress:() => console.log('确定了')},
        ])
      }
      <Button title={'按钮'} onPress={onPressed}></Button>
    ```
    ### 3.5 TextInput
    ```js
      <TextInput autoCapitalize={"none"} autoFocus={true} autoCorrent={false} returnKeyType={'search'} placeholder={'通过关键词搜索'}
        placeholderTextColor={'#77'}
        onSubmitEditing={(event) => {
          const keyword = event.nativeEvent.text
          const searchKeyword = keyword.trim().toLowerCase()
          if(!searchKeyword){
            Alert.alert('提示',"请输入搜索关键词")
          }
        }}
      ></TextInput>
    ```
---
## 五、列表组件SectionList和FlatList
  > 和一般化用途的ScrollView不同，SectionList和FlatList只会渲染**当前屏幕可见**的元素，这样有利于显示大量的数据。
  ### 5.1 FlatList组件
  > 按需渲染长列表数据
  - renderItem
  - data
  - extraData:向FlatList传递extraData={selectedId}可以确保当selectedId变化时FlatList会重新渲染
  - refershControl
  - ItemSeparatorComponent:item分割组件
  - ListEmptyComponent:无数据空组件
  - onEndReached触底加载更多
  - ListFooterComponent:配合onEndReached触底加载更多，触底没有数据的时候使用
    ```js 
      let [refresh, setRefresh] = useState(true)
      const onRefresh = () => {
        setRefreshing(true)
      }
      const onEndReached = () => {
        console.log('正在加载更多数据')
      }
      <SafeAreaView>
        <FlatList
          data={data}
          renderItem={renderItem}
          keyExtractor={item => item.id}
          ListHeaderComponent={}
          ListFooterComponent={}
          refershControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={'#1f99b0'}>}
          onEndReached={onEndReached}
          onEndReachedThreshold={0.1}
          horizontal={true}
          showsHorizontalScrollIndicator={true}
          renderItem={renderItem}
          ItemSeparatorComponent={renderSeparator}
          ListEmptyComponent={<NoData></NoData>}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tinyColor={"#1f99b0"}></RefreshControl>
          >
        </FlatList>
      </SafeAreaView>
    ```
  ### 5.2 SectionList
---
## 六、其他相关组件
  ### 6.1 StatusBar
  ### 6.2 ActivityIndicator
  ```js
    <ActivityIndicator color="green" size={2-}></ActivityIndicator>
  ```
  ### 6.3 TouchableHighlight,TouchableOpacity,TouchableWithoutFeedback
  ```js
    <TouchableHighlight onPress={onReject}><Text>触碰高亮</Text></TouchableHighlight>
    <TouchableOpacity onPress={onAccept}><Text>触碰透明度变化</Text></TouchableOpacity>
    <TouchableWithoutFeedback onPress={onAccept}><Text>触碰无任何变化</Text></TouchableWithoutFeedback>
  ```
---
## 七、其他API
  ### 7.1 Platform
  - platform.os
  ### 7.2 Dimensions
  ```js
    const windowWidth = Dimensions.get('window').width;
    const windowHeight = Dimensions.get('window').height;
    const styles = StyleSheet.create({
      itemImage:{
        height:200,
        width:Dimensions.get('window').width,
        marginVertical:20
      }
    })
  ```
  ### 7.3 Animated
---
## 八、ScrollView，SafeAreaView,FlatList和RefreshControl
  ### 8.1 ScrollView使用
  - showVerticalScrollIndicator:隐藏滚动条
  - contentContainerStyle:设置ScrollView内部容器样式
  ### 8.2 SafeAreaView组件
  > 官方已经弃用，使用**react-native-safe-area-context**插件;
  > 防止ios设备的刘海挡住ScrollView
  ### 8.3 ScrollView搭配RefreshControl组件使用
  ```js
    let [refresh, setRefresh] = useState(true)
    const onRefresh = () => {
      setRefreshing(true)
    }
    <SafeAreaView>
      <ScrollView refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={'#1f99b0'}>}>
        <Text></Text>
      </ScrollView>
    </SafeAreaView>
  ```
  ### 8.4 RefreshControl下拉刷新组件
  > 这一组件可以用在 ScrollView 或 FlatList 内部，为其添加下拉刷新的功能。当 ScrollView 处于竖直方向的起点位置（scrollY: 0），此时下拉会触发一个onRefresh事件。
  ```js
    const [refreshing, setRefreshing] = useState(false)
    const onRefresh = () => {
        setRefreshing(true)
      setTimeout(() => {
        setRefreshing(false)
      }, 3000);
    }
    <ScrollView style={styles.container} refreshControl={
      <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tinyColor={"#1f99b0"}></RefreshControl>
    }>
      <View style={styles.slides}>
        <FlatList data={recommandData} keyExtractor={item => item.id} renderItem={renderItem} horizontal={true} showsHorizontalScrollIndicator={true}></FlatList>
      </View>
    </ScrollView>
  ```
## 九、第三方组件
  ### 9.1 WebView
  > npx expo install react-native-webview
  - **useAgent**:识别来源
  - **onShouldStartLoadWithRequest**超链接拦截，防止webView内路由跳转无法在webView中返回的问题
  ```js
    import * as WebBrowser from 'expo-web-browser'
    /**
     * 超链接拦截
     */
    const onShouldStartLoadWithRequest = (request) => {
      // props.source.uri是webview初始加载的地址
      // request.url是点击链接后，要访问的地址
      // 如果相同，则表示允许使用WebView加载
      if(props.source?.uri === request.url){
        return true
      }
      // 否则，用webBrowser在外部浏览器打开链接
      void WebBrowser.openBrowserAsync(request.url)
    }
  ```
  ### 9.2 Picker
  > @react-native-picker/picker
  ```js
    <Picker selectedValue={color} onValueChange={(itemValue, itemIndex) => setColor({color: itemValue})}>
      <Picker.Item label="白色" value="white"></Picker.Item>
      <Picker.Item label="红色" value="red"></Picker.Item>
    </Picker>
  ```
  ### 9.3 Swiper
  ```js
    <Swiper>
      <Image require={}></Image>
    </Swiper>
  ```
  ### 9.4 AsyncStorage
  > npx expo install @react-native-async-storage/async-storage
  ```js
    export function setStorage (key, value) {
      AsyncStorage.setItem(key, JSON.stringify(value))
    }
  ```
  ### 9.5 Geolocation
  > npx expo install @react-native-community/geolocation
  ```js
    Geolocation.getCurrentPosition(
      info => console.log(info),
      error => Alert.alert('报错', JSON.stringify(error)),
      {timeout:1000}
    )
  ```
  ### 9.6 Camera
  > npm install react-native-cameta,支持拍照，录视频，人脸识别，扫码
  ```js
    import {RNCamera} from 'react-native-camera'
  ```
  ### 9.7 ImagePicker
  ```js
    changeImage = () => {
      ImagePicker.showImagePicker(options, (res) => {
        if (res.didCancel){
          console.log('user cancelled image picker')
        } else if (res.error) {
          console.log('Image ImagePickerResponse.customButton')
        } else if (res.customButton) {
          console.log("user tapped custom button",res.customButton)
        } else {
          const source = {uri:res.uri}
          console.log(source)
        }
      })
    }
  ```
  ### 9.8 react-navigation
    - stack
    - Link和Button组件
    - useNavigation().navigate()
    - useNavigation().push()
    - useNavigation().goBack()
    - useNavigation().popTo()
    - useNavigation().popToTop()
  ```js
    import {createStaticNavigation, useNavigation} from '@react-navigation/native';
    import { Link } from '@react-navigation/native';
    import { Button } from '@react-navigation/elements';

    function HomeScreen() {
      const navigation = useNavigation();
      return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
          <Text>Home Screen</Text>
          <Link screen="Details">Go to Details</Link>
          <Button screen="Details">Go to Details</Button>
          <Button onPress={() => navigation.navigate('Details')}>Go to Details</Button>
          <Button onPress={() => navigation.push('Details')}>Go to Details... again</Button>
          <Button onPress={() => navigation.goBack()}>Go back</Button>
          <Button onPress={() => navigation.popTo('Home')}>Go to Home</Button>
          <Button onPress={() => navigation.popToTop()}>Go back to first screen in stack</Button>

        </View>
      );
    }
  ```
  ### 9.9 bottomTopNavigator
  > npm i @react-navigation/bottom-tabs
  ```js
    import {createBottomTopNavigator} from '@react-navigation/bottom-tabs'
    const tab = createBottomTopNavigator()
  ```
  ### 9.10 图标组件库
  > react-native-vector-icons
  > @expo/vector-icons
  ### 9.11 Drawer导航
  > npm i @react-navigation/drawer
  ### 9.12 MaterialTopTap导航
  > npm install @react-navigation/material-top-tabs
---
## 十、React Navigator
> npm install react-native-screens react-native-safe-area-context
> npx expo install react-native-screens react-native-safe-area-context

## 模态框Modal
## WebView
  
  ### 访问网页的三种方式：Linking,WebBrowser与WebView
  - npx expo install expo-linking，跳转到别的地方
  - npx expo install expo-web-browser,底部弹出，不会跳转到别的连接
  - npx expo install react-native-webview,参考下面的ProgressWebView组件
  ```js
    import * as Linking from 'expo-linking'
    <View onPress={()=>{linking.openURL("https://xxx")}}></View>
    import * as WebBrowser from 'expo-web-browser'
    <View onPress={async()=>{ await WebBrowser.openBrowserAsync("https://xxx")}}></View>
  ```
  ### webview去除页头页脚
  ### 封装ProgressWebView组件：webView添加表示页面加载的进度条，从而防止页面加载前空白的问题
  ```js
    const ProgressBar = (props) => {
      const width = `${props.progress * 100}%`
      return <View style={[styles.loadingBar, {width]}></View>
    }
    /**
    带有加载中和进度条的webview
     */
    export default function ProgressWebView (props) {
      const [progress, setProgress] = useState(0)

      return (
        <View style={style={style.container}}>
          <ProgressBar progress={progress}></ProgressBar>
          <WebView
            useAgent="my-app"
            source={{uri:"https://xxx"}
            startInLoadingState={true}
            renderLoading={()=><Loading></Loading>}
            onLoadProgerss ={({nativeEvent})=>{
              setPreogress(nativeEvent.progress) 
            }}
            onShouldStartLoadWithRequest={onShouldStartLoadWithRequest}
            {...props}
          >
          </WebView>
        </View>
      )
    }
  ```

## 分享
```js
const onShare = async () => {
  const url = ''
  const message = Platform.OS == 'ios'? course.name : `${course.name}:\n${url}`
  await Share.share({
    message,
    url
  })
}
```
# react-native-side-menu侧边栏
> npx expo install react-natice-side-menu-updated
# 自定义封装expo-video视频播放器
> npx expo install expo-screen-orientation expo-navigation-bar expo-device @react-native-community/slider react-native-safe-area-context

# react-native-keyword-controller键盘自动避让表单
> npx expo install react-native-keyword-controller react-native-reanimated react-native-worklets
# useFocusEffect
  ```js
    useFocusEffect(
      useCallback(() => {
        async function checkReload(){
          await onReload()
        }
        void checkReload()
      },[])
    )
  ```

# figma制作应用图标和启动屏expo-splash-screen
```js
  ios:{

  }
```
# EAS云打包
- npm i -g eas-cli
- eas login
- eas build:configure
- npx expo-doctor
- eas build --platform ios
- eas build --platform android
```js
  // 安卓
  production:{
    android:{
      buildType:"apk"
    }
  }
```