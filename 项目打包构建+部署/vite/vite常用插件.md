# 一：插件API

# 二：自定义插件
  ```js
    export default (enforce?: 'pre' | 'post') => {
      return {
        name: 'test',
        enforce,
        buildStart: () => {
          console.log('buildStart',enforce)
        },
        resolveId: () => {
          console.log('resolveId', enforce)
        },
        load () {
          console.log('load')
        }
      }
    }
  ```

# 三：vite的插件特有钩子
  ```js
    // config
    // configResolved
  ```
# 三：常用插件

  ### 1.rollup-plugin-visualizer：分析打包依赖
  ### 2.@rollup/plugin-commonjs：支持commonJS规范
  ### 3.unplugin-auto-import/vite: 自动导入
  ### 4.unplugin-vue-components/resolvers: 自动导入elementPlus


# 四：vite的plugin使用
 ```js
    // 第一步：新建vite/plugins/index.js文件
    import vue from '@vitejs/plugin-vue'
    import commonjs from '@rollup/plugin-commonjs'

    import createAutoImport from './auto-import'
    import createSvgIcon from './svg-icon'
    import createCompression from './compression'
    import createSetupExtend from './setup-extend'

    export default function createVitePlugins(viteEnv, isBuild = false) {
      const vitePlugins = [commonjs(), vue()]
      vitePlugins.push(createAutoImport())
      vitePlugins.push(createSetupExtend())
      vitePlugins.push(createSvgIcon(isBuild))
      vitePlugins.push(components({
        resolvers: [ElementPlusResolver()],
      }))
      isBuild && vitePlugins.push(...createCompression(viteEnv))
      return vitePlugins
    }
    // 第二步：新建auto-import等文件...引入插件
    // ======================auto-import.ts======================
    import autoImport from 'unplugin-auto-import/vite'
    import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
    export default function createAutoImport() {
        return autoImport({ 
            resolvers: [ElementPlusResolver()],
            imports: [
                'vue',
                'vue-router',
                'pinia'
            ],
            dts: false
        })
    }
    // ======================setup-extend.ts======================
    import setupExtend from 'unplugin-vue-setup-extend-plus/vite'
    export default function createSetupExtend() {
        return setupExtend({})
    }
    // ======================svg-icon.ts======================
    import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
    import path from 'path'
    export default function createSvgIcon(isBuild) {
        return createSvgIconsPlugin({
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons/svg')],
            symbolId: 'icon-[dir]-[name]',
            svgoOptions: isBuild
        })
    }
    // ======================compression.ts======================
    import compression from 'vite-plugin-compression'
    export default function createCompression(env) {
        const { VITE_BUILD_COMPRESS } = env
        const plugin = []
        if (VITE_BUILD_COMPRESS) {
            const compressList = VITE_BUILD_COMPRESS.split(',')
            if (compressList.includes('gzip')) {
                // http://doc.ruoyi.vip/ruoyi-vue/other/faq.html#使用gzip解压缩静态文件
                plugin.push(
                    compression({
                        ext: '.gz', // 文件后缀名
                        deleteOriginFile: false,
                        threshold: 1025 * 3 // 体积大于多少才会压缩
                    })
                )
            }
            if (compressList.includes('brotli')) {
                plugin.push(
                    compression({
                        ext: '.br',
                        algorithm: 'brotliCompress',
                        deleteOriginFile: false
                    })
                )
            }
        }
        return plugin
    }
    // =============element-plus的自动导入
    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()],
        imports: ["vue", "vue-router", "pinia"],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
    ],

    // 第三步：在vite.config.js中引入插件
    import createVitePlugins from './vite/plugins'

    export default defineConfig(({ mode, command }) => {
      const env = loadEnv(mode, process.cwd())
      const { VITE_APP_BASE_PATH, VITE_APP_BASE_API, VITE_APP_BASE_URL } = env
      return {
        // 默认情况下，vite 会假设你的应用是被部署在一个域名的根路径上
        // 例如 https://www.ruoyi.vip/。如果应用被部署在一个子路径上，你就需要用这个选项指定这个子路径。例如，如果你的应用被部署在 https://www.ruoyi.vip/admin/，则设置 baseUrl 为 /admin/。
        base: VITE_APP_BASE_PATH,
        plugins: createVitePlugins(env, command === 'build')
      }
    })
  ```