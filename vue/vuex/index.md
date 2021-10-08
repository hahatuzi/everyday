# vuex使用思考：在做自建站项目时发现要想实现数据的完全增删改查自由，使用普通的数据传递方法有点冗余，故最后选择vuex方案管理数据，实现数据自由。
1.matation中不能返回数据，即不能return,但getters中可以处理数据并返回结果。
2.从后端请求数据，再返回到state的处理方法。
dispatch ---> action ---> matation ---> state