## style样式
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
## Text
  - numberOfLines:文本超出一行时，用几行来显示它
## ScrollView
  ### (1)ScrollView使用
  ### (2)SafeAreaView组件
  > 防止ios设备的刘海挡住ScrollView
  ### (3)ScrollView搭配RefreshControl组件使用
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
  ### contentContainerStyle:设置ScrollView内部容器样式
## RefreshControl下拉刷新组件
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
## FlatList组件
  > 按需渲染长列表数据
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
## Switch
## Alert
  ```js
  const onPressed = () => {
    Alert.alert('提示信息','请问确定删除以下数据吗',[
      {text:"取消",onPress:() => console.log('取消了')},
      {text:"确定",onPress:() => console.log('确定了')},
    ])
  }
    <Button title={'按钮'} onPress={onPressed}></Button>
  ```
## Dimensions
  ```js
    const {width, height} = Dimensions.get('window')
  ```
## StatusBar
## Image
  > expo的Image组件和ReactNative的Image组件的区别：Expo功能更多
## 模态框Modal
## WebView
  > npx expo install react-native-webview
  ### useAgent识别来源
  ### onShouldStartLoadWithRequest 超链接拦截，防止webView内路由跳转无法在webView中返回的问题
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
# react-native-side-menu