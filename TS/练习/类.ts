class person {
  private _name:string;
  age:number;
  constructor(name:string,age:number) {
    this._name = name
    this.age = age
  };
  get name () {
    return this._name
  }
}
const per = new person('lisa', 18)
console.log(per.name)
console.log(per.age)

class C{
  constructor(public name:string, public age:number){

  }
}
class UserAPI {
  /**
   * 登录成功后获取用户信息（昵称、头像、权限集合和角色集合）
   *
   * @returns 用户信息
   */
  static getInfo() {
    return request<any, UserInfo>({
      url: `${USER_BASE_URL}/me`,
      method: "get",
    });
  }
}
// 使用
UserAPI.getInfo()

class Point {
  x:number;
  y:number;
  constructor(x:number, y:number){
    this.x = x
    this.y = y
  }
} 
interface PonitINterface {
  x:number,
  y:number
}

interface Point3D extends Point {
  z:number
}

class Father {
  readonly name:String
  constructor(name:string){
    this.name = name
  }
}
class Son extends Father{
  getName () {
    console.log(this.name)
  }
}