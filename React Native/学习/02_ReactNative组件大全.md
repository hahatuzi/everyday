## style样式
  ```js
  // 数组类型
  <view style={[{fontSize:50},styles.title]}></view>
  ```
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
## FlatList组件
  > 按需渲染长列表数据
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
        onEnDReachedThreshold={0.1}
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