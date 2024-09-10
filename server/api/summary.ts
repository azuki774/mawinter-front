export default defineEventHandler (async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  const url = config.public.mawinterApi + '/v2/record/summary/' + query.year
  const result = await $fetch(url,
    {
      method: 'GET',
    },
  )
  return result
})
