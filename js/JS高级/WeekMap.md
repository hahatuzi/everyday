# WeekMap
WeekMap类似于Map,都是键值对，但是WeekMap**只有对象能够作为键**，且键是弱引用的，
如果一个对象只被WeakMap引用，那么这个对象**可以被垃圾回收（GC）**。当这个对象被垃圾回收后，它对应的键值对也会从WeakMap中自动移除。
WeekMap**不能遍历**