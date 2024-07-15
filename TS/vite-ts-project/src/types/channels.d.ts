export type Channels = {
  id:number,
  name:string
}
export type ResData = {
  data: {
    channel: Channels[]
  },
  msg:string
}
