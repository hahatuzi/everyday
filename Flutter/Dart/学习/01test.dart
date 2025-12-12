void main (List<String> args) {
  print('Hello World');
  // const num = 10;
  // final time = DateTime.now();
  // var name = 'lisa';
  // String text = '我是${name}';
  // double count = 1.6;
  // int count1 = 2;
  // count1 = count.toInt();
  // count = count1.toDouble();
  // bool isFinish = false;
  // print(count1, count, isFinish);
  // List list = ['张三', 12, 'rose', 'lisa', 34, 'jennie','jisoo', '12'];
  // // list.removeRange(0,2);
  // // list.removeLast();
  // // list.remove(34);
  // print(list);
  // bool isNew = list.every((item) {
  //   return item.toString().startsWith('小');
  // });
  // print(isNew);
  // print(list.last);
  // print(list.first);
  // print(list.isEmpty);
  // print(list.length);
  // print(list.where((item){
  //   return item.toString().startsWith('j');
  // }));

  // Map obj = {'name':'lisa'};
  // obj.forEach((key, value) {
  //   print('${key}-${value}');
  // });
  // obj.addAll({'age': 28});
  // print(obj.containsKey('age'));

  // dynamic free = 12;
  // free = 'free';
  // print(free);

  // String? username = null;
  // print(username?.startsWith('新')); // null
  // String displayName = username ?? 'lisa';
  // print(displayName); // 'lisa'

  // int add (int a, int b) {
  //   return a + b;
  // };
  // print(add(3,4));

  // String combine (String a, [String? b, String? c]) {
  //   return a + (b ?? '' ) + ( c ?? ''); 
  // };
  // print(combine('lisa', '--'));

  // Function test = () {
  //   print('test');
  // };
  // test();
  // Person p = Person(name:"lisa",age:28,sex:'女');
  // p.study();
  Child c = Child(name:'lisa',age:20);
  c.study();
  Pay p1 = WXPay();
  Pay p2 = ALIPay();
  p1.pay();
  p2.pay();
}

class Person {
  String? name = 'lisa';
  int? age = 0;
  String? sex = '男';
  Person ({String?name,int? age, String?sex}) {
    this.name = name;
    this.age = age;
    this.sex = sex;
  }
  void study(){
    print('姓名${name}年龄${age}性别${sex}');
  }

}

class Parent {
  String? name;
  int? age;
  Parent({this.name, this.age});
  void study () {
    print('父类-${name}在学习');
  }
}

class Child extends Parent {
  Child({String? name, int? age}) : super(name:name,age:age);
  @override
  void study() {
    // super.study();
    print('子类${name}年龄${age}');
  }
}

abstract class Pay {
  void pay();
}
class WXPay implements Pay {
  @override
  void pay() {
    print('微信支付');
  }
}
class ALIPay implements Pay {
  @override
  void pay() {
    print('支付宝支付');
  }
}