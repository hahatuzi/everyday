## 一、集合体系
  ### 1.1 Collection体系概述
  > Collection是一个结构，我们不能直接创建它的对象。只能创建它实现类的对象，比如ArrayList.
  > Collection是List，Set和Queue的**父接口**。**List**集合添加的元素是**有序，可重复，有索引的**。**Set**添加的是**无序的，不重复的，无索引的**
  - Collection
    - List
      - ArrayList
      - LinkedList
    - Set
      - TreeSet
      - HashSet
        - LinkedHashSet
  ### 1.2 Collection集合的方法
  |  方法                   	|作用	                                |返回值   |
  |boolean add(E e)          	|添加单个元素，成功返回 true          |	boolean |
  |boolean remove(Object o)		|删除指定元素（找到第一个匹配的）   	|	boolean |
  |void clear()	             	|清空集合所有元素，集合对象本身还在 	|	void    |
  |boolean contains(Object o)	|判断是否包含该元素，底层是equals方法 | boolean |
  |boolean isEmpty()	      	|判断集合是否为空（size=0）         	|	boolean |
  |int size()	              	|获取集合中元素个数	                	| int     |
    ```java
      package com.collection;

      import java.util.ArrayList;
      import java.util.Collection;

      public class A01_Collection {
          public static void main(String[] args){
              Collection<String> col = new ArrayList<>();
              col.add("a");
              col.add("b");
              col.add("c");
              System.out.println(col);
              col.remove("b");
              boolean res = col.contains("b");
              System.out.println(res);
          }
      }
    ```
    ### 1.3 Collection的遍历方式
    |  遍历方法   	|Collection	  |List    |
    |迭代器         |             |	boolean |
    |列表迭代器     |            	|	boolean |
    |增强for       	|            	|	void    |
    |Lambda表达式	  |             | boolean |
    |普通for循环	  |            	|	boolean |
      #### (1)迭代器：
      - 如果当前位置没有元素，还要强行获取，会报NoSuchElementException
      - 迭代器遍历完毕，指针不会复位
      - 循环中只能用一次next方法
      - 迭代器遍历时，不能用集合的方法进行增加或者删除
        ```java
          package com.collection;
          import java.util.ArrayList;
          import java.util.Collection;
          import java.util.Iterator;

          public class A01_Collection {
            public static void main(String[] args){
                Collection<String> col = new ArrayList<>();
                col.add("a");
                col.add("b");
                col.add("c");
                Iterator<String> it = col.iterator();
                while(it.hasNext()){
                    String str = it.next();
                    System.out.println(str);
                }
            }
          }
        ```
      #### (2)增强for
      > 修改增强for中的变量，不会改变集合中原本的数据。
        ```java
          for (String s:col){
            s = 'qq';
          }
        ```
      #### (3)forEach
---
  ### 1.4 List集合
  - **void add(int index, E elemnt)**:在指定位置插入指定的元素
  - **E remove(int index)**,在调用方法的时候，如果方法出现了重载现象，优先调用实参和形参一致的那个方法
  - **E set(int index, E element)**,修改指定索引处的元素，返回被修改的元素
  - **E get(int index)**,返回指定索引处的元素
    #### List集合的遍历方式
    - 迭代器遍历:遍历的时候可以删除元素
    - 列表迭代器：遍历的时候可以添加元素
    - 增强for
    - lambda表达式
    - 普通for
      ```java
        package com.collection;
        import java.util.ArrayList;
        import java.util.List;

        public class A02_Collection {
            public static void main(String[] args){
                List<Integer> list = new ArrayList<>();
                list.add(1);
                list.add(2);
                list.add(3);
                list.remove(1);
                System.out.print(list);// [1, 3]
                // 手动将基本数据类型的1转为Integer类型
                Integer i = Integer.valueOf(2);
                list.remove(i);

                // 第一种：迭代器遍历
                Iterator<String> it = list.iterator();
                while(it.hasNext()){
                  string str = it.next();
                  System.out.println(str);
                }
                // 第二种：增强for
                for(String s : list){
                  System.out.println(s);
                }
                // 第三种：Lambda表达式
                list.forEach(s -> System.out.println(s));
                // 第四种：普通for循环
                for (int i = 0; i < list.size(); i++){
                  String s = list.get(i);
                  System.out.println(s);
                }
                // 第五种：列表迭代器
                ListIterator<String> it = list.listIterator()
                while(it.hasNext()){
                  String str = it.next();
                  System.out.println(str);
                }
            }
        }
      ```
  ### 1.5 ArrayList集合
  #### ArrayList集合的底层原理
  - 利用空参创建的集合，在底层创建 一个默认长度为0的数组
  - 添加第一个元素时，底层会创建一个新的长度为10的数组
  - 存满时，会扩容1.5倍
  - 如果一次添加多个元素，1.5倍还放不下，则新创建数组的长度以实际为准
  ### LinkedList集合
  > 底层是双链表，查询慢，首尾操作快
  - plulic void addFirst(E e)
  - plulic void addLast(E e)
  - plulic void getFirst(E e)
  - plulic void getLast(E e)
  - plulic void removeFirst(E e)
  - plulic void removeLast(E e)
    ```java
      private static class Node<E> {
        E item;
        Node<E> next;
        Node<E> prev;
        Node(Node<E> prev, E element, Node<E> next){
          this.item = element;
          this.prev = prev;
          this.next = next;
        }
      }
    ```