function LinkedList () {
      // 内部的节点类
      function Node (data) {
        this.val = data
        this.next = null
      }
      this.head = null
      this.length = 0

      LinkedList.prototype.append = function (data) {
        let node = new Node(data)
        if (this.length == 0) {
          this.head = node
        } else {
          let lastNode = this.head
          while (lastNode.next) {
            lastNode = lastNode.next
          }
          lastNode.next = node
        }
        this.length+=1
      }
      // toString()
      LinkedList.prototype.toString = function () {
        let res = ''
        if (this.length != 0) {
          let curNode = this.head
          while (curNode) {
            res += curNode.data
            curNode = curNode.next
          }
        }
        return res
      }
      // insert
      LinkedList.prototype.insert = function (position, data) {
        if (position < 0 || position > this.length) return false
        let newNode = new Node(data)
        if (position == 0) {
          newNode.next = this.head
          this.head = newNode
        } else {
          let index = 0
          let curNode = this.head
          let previousNode = null
          while (index < position) {
            index++
            previousNode = curNode
            curNode = curNode.next
          }
          newNode.next = curNode
          previousNode.next = newNode
        }
        this.length+=1
      }
      // get
      LinkedList.prototype.get = function (position) {
        if (position < 0 || position > this.length) return false
        let index = 0
        let curNode = this.head
        while (index++ < position) {
          curNode = curNode.next
        }
        return curNode.val
      }
      // indexOf
      LinkedList.prototype.indexOf = function (data) {
        let index = -1
        let curNode = this.head
        while (curNode) {
          if(curNode.val == data) return index
          index += 1
          curNode = curNode.next
        }
        return index
      }
      // update
      LinkedList.prototype.update = function (position, data) {
        if (position < 0 || position > this.length) return false
        let index = 0
        let curNode = this.head
        while (index++ < position) {
          curNode = curNode.next
        }
        curNode.val = data
        return curNode
      }
      // removeAt
      LinkedList.prototype.removeAt = function (position) {
        if (position < 0 || position > this.length) return false
        if (position == 0) {
          this.head = this.head.next
        } else {
          let index = 0
          let curNode = this.head
          let previousNode = null
          while (index++ < position) {
            previousNode = curNode
            curNode = curNode.next
          }
          previousNode.next = curNode.next
        }
        this.length--
      }
      // remove
      LinkedList.prototype.remove = function (data) {
        // let index = -1
        let curNode = this.head
        let previousNode = null
        while (curNode.val != data) {
          previousNode = curNode
          curNode = curNode.next
        }
        previousNode.next = curNode.next
        this.length--
      }
      // isEmpty
      LinkedList.prototype.isEmpty = function () {
        return this.length == 0
      }
      // isEmpty
      LinkedList.prototype.size = function () {
        return this.length
      }
    }