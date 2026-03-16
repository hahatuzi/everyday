function BinarySearchTree () {
  this.root = null
  function Node (key) {
     this.key = key
     this.left = null
     this.right = null
  }
  BinarySearchTree.prototype.insert = function (key) {
    let node = new Node(key)
    if(this.root === null) {
      this.root = node
    } else {
      this.insertNode(this.root, node)
    }
  }
  BinarySearchTree.prototype.insertNode = function (node, newNode) {
    if(node.key > newNode.key) {
      if(node.left === null) {
        node.left = newNode
      } else {
        this.insertNode(node.left, newNode)
      }
    } else {
      if(node.right === null) {
        node.right = newNode
      } else {
        this.insertNode(node.right, newNode)
      }
    }
  }
  // 栈版本--先序遍历
  BinarySearchTree.prototype.preOrderTraversal1 = function () {
    if (this.root === null) return []
    let stack = [this.root]
    let arr = []
    while(stack.length !== 0) {
      let node = stack.pop()
      if (node !== null) {
        arr.push(node.key)
        stack.push(node.right)
        stack.push(node.left)
      }
    }
    return arr
  }
  BinarySearchTree.prototype.midOrderTraversal1 = function (){
    if (this.root === null) return []
    let stack = []
    let arr = []
    let curNode = this.root
    while(stack.length !== 0 || curNode) {
      while (curNode !== null) {
        stack.push(curNode)
        curNode = curNode.left
      }
      const node = stack.pop()
      arr.push(node.key)
      curNode = node.right
    }
    return arr
  }
  // 递归版本--先序遍历
  BinarySearchTree.prototype.preOrderTraversal = function (handler) {
    this.preOrderTraversalNode(this.root, handler)
  }
  BinarySearchTree.prototype.preOrderTraversalNode = function (node, handler){
    if(node !== null) {
      handler(node.key)
      this.preOrderTraversalNode(node.left, handler)
      this.preOrderTraversalNode(node.right, handler)
    }
  }
  BinarySearchTree.prototype.midOrderTraversal = function (handler) {
    this.midOrderTraversalNode(this.root, handler)
  }
  BinarySearchTree.prototype.midOrderTraversalNode = function (node, handler) {
    if (node != null){
      // 1.处理左子节点
      this.midOrderTraversalNode(node.left, handler)
      handler(node.key)
      // 1.处理右子节点
      this.midOrderTraversalNode(node.right, handler)
    }
  }
}