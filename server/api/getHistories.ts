export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  const params: { [key: string]: string } = {}
  if (query.yyyymm != undefined) {
    params.yyyymm = String(query.yyyymm)
  }
  if (query.category_id != undefined) {
    params.category_id = String(query.category_id)
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
