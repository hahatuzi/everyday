# useDeferredValue
  > 允许延迟更新UI的非关键部分，以让其他部分先更新
  ```js
    function SearchPage() {
      const [query, setQuery] = useState('');
      const deferredQuery = useDeferredValue(query);
      // ...
    }
  ```