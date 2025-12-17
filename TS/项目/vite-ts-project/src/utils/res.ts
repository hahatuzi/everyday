// if (code === 403) {
//   if (!isRelogin.show) {
//     isRelogin.show = true;
//     ElMessageBox.confirm('登录状态已过期，您可以继续留在该页面，或者重新登录', '系统提示', { confirmButtonText: '重新登录', cancelButtonText: '取消', type: 'warning' }).then(() => {
//       isRelogin.show = false;
//       useUserStore().logOut().then(() => {
//         router.replace({ path:  "/login"});
//       })
//     }).catch(() => {
//       isRelogin.show = false;
//     });
//   }
//   throw new Error('无效的会话，或者会话已过期，请重新登录。')
// } else if (code === 500) {
//   ElMessage({ message: msg, type: 'error' })
//   throw new Error(msg)
// } else if (code === 601) {
//   ElMessage({ message: msg, type: 'warning' })
//   throw new Error(msg)
// } else if (code !== 200) {
//   ElNotification.error({ title: msg })
//   throw new Error(msg)
// } else {
//   return  Promise.resolve(res.data)
// }
type Res = {
  code:Code,
  msg:string
}

type Code = 200 | 601 | 500 | 403
const code:Code = 200

const res:Res = {
  code:200,
  msg:'调用成功'
}
console.log(res)
