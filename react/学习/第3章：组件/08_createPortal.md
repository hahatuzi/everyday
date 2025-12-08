# 基本使用
  ```js
    // createPortal 允许你将 JSX 作为 children 渲染至 DOM 的不同部分。
    // 调用 createPortal 创建 portal，并传入 JSX 与实际渲染的目标 DOM 节点：
    import { createPortal } from 'react-dom';

    // ...

    <div>
      <p>这个子节点被放置在父节点 div 中。</p>
      {createPortal(
        <p>这个子节点被放置在 document body 中。</p>,
        document.body
      )}
    </div>
  ```