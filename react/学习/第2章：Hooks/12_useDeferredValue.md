# useDeferredValue
  ```js
    function SearchPage() {
      const [query, setQuery] = useState('');
      const deferredQuery = useDeferredValue(query);
      // ...
    }
  ```