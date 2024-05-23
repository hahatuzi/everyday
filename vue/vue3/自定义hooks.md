# 自定义hooks使用场景
  ```js
    import { ref, onMounted, onUnmounted } from 'vue';

    export function useMousePosition() {
      const x = ref(0);
      const y = ref(0);

      function updatePosition(event) {
        x.value = event.clientX;
        y.value = event.clientY;
      }

      onMounted(() => {
        window.addEventListener('mousemove', updatePosition);
      });

      onUnmounted(() => {
        window.removeEventListener('mousemove', updatePosition);
      });

      return { x, y };
    }
  ```
  使用该hook
  ```js
    <template>
      <div>
        Mouse position: X={{ x }}, Y={{ y }}
      </div>
    </template>

    <script setup>
    import { useMousePosition } from './useMousePosition';

    const { x, y } = useMousePosition();
    </script>
  ```
### 2.useCout
```js
import {ref, moMounted, computed} from 'vue'
export default function useCount {
  const count = ref(0)
  const doubleCount = computed(() => count * 2)
  const increase = (delta => {
    return count.value + delta
  })
  return {
    count,
    doubleCount,
    increasa
  }
}
```
使用
```js
<script setup lang="ts">
    import useCount from "@/hooks/useCount";
    const { count,doubleCount,increase } = useCount;
    const newCount = increase(10); // 输出: 10       
</script>
```
