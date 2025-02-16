export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  const params: {
    yyyymm: string
    category_id: string
  } = {
    yyyymm: String(query.yyyymm),
    category_id: String(query.category_id),
  }
  const queryParams = new URLSearchParams(params)
  const url = config.public.mawinterApi + '/v2/record?' + queryParams
  const result = await $fetch(url,
    {
      method: 'GET',
    },
  )
  return result
})
