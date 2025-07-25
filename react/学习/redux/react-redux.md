useSelector:用来加载state中的数据
# 一：vite项目中使用react-redux
  ### 第一步：npm i react-redux --save
  ### 第二步：创建store文件夹，
  ```js
  import { legacy_createStore} from 'redux'
  import reducer from './reducer/index.ts'

  const store = legacy_createStore(reducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
  export default store
  ```
  ### 第三步：在main.js中添加配置
  ```js
    import { Provider } from 'react-redux'
    <Provider store={store}>
      <BrowserRouter>
          <ConfigProvider locale={zhCN}>
            <App />
          </ConfigProvider >
      </BrowserRouter>
    </Provider>
  ```


# 二：浏览器redex-dev-tools使用
  ### 第一步：在项目中创建types文件夹，并在它的下面创建store.d.ts文件,声明tools工具变量，
  ```js
    type RootState = ReturnType<typeof import("@/store").getState>
    interface Window{
      __REDUX_DEVTOOLS_EXTENSION__:function
    }
  ```
  ### 第二步：在vite-env.d.ts文件中添加ts声明文件
  ```js
    /// <reference types="vite/client" />
    declare module '*.ts'
  ```


# 三：reducer的模块化和组合
  ### 第一步:在store文件夹下创建reducer文件夹  -->  index.ts
  ```js
    import { AnyAction } from "redux";
    import { GlobalState } from "@/redux/interface";
    // import { changeTheme } from "@/hooks/useTheme";
    import produce from "immer";
    import * as types from "@/redux/mutation-types";

    const globalState: GlobalState = {
      token: "",
      userInfo: "",
      assemblySize: "middle",
      language: "",
      themeConfig: {
        // 默认 primary 主题颜色
        primary: "#1890ff",
        // 深色模式
        isDark: false,
        // 色弱模式(weak) || 灰色模式(gray)
        weakOrGray: "",
        // 面包屑导航
        breadcrumb: true,
        // 标签页
        tabs: true,
        // 页脚
        footer: true
      }
    };

    // global reducer
    const global = (state: GlobalState = globalState, action: AnyAction) =>
      produce(state, draftState => {
        switch (action.type) {
          case types.SET_TOKEN:
            draftState.token = action.token;
            break;
          case types.SET_ASSEMBLY_SIZE:
            draftState.assemblySize = action.assemblySize;
            break;
          case types.SET_LANGUAGE:
            draftState.language = action.language;
            break;
          case types.SET_THEME_CONFIG:
            // changeTheme(action.themeConfig.primary);
            draftState.themeConfig = action.themeConfig;
            break;
          default:
            return draftState;
        }
      });

    export default global;

    // idnex.ts文件中暴露reducer
    import { combineReducers} from 'redux'
    import num from './num'

    const reducer = combineReducers({
      num
    })
    export default reducer
  ```
  ### 第二步：在store -->的index.ts文件中引入reducer
  ```js
  import { legacy_createStore} from 'redux'
  import reducer from './reducer/index.ts'

  const store = legacy_createStore(reducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
  export default store
  ```
