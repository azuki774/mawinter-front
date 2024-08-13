export default defineEventHandler ( async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  // create body
  const reqbody = `
  {
  "category_id":${query.category_id},
  "price":${query.price},
  "from":"mawinter-fe",
  "memo":"手動"
  }
  `
  console.log(reqbody)
  const url = config.public.mawinterApi + "/v2/record"
  const result = await $fetch(url,
    {
        method: "POST",
        body: reqbody
    }
  )
  return result
})
