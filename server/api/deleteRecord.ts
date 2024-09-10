export default defineEventHandler (async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  const url = config.public.mawinterApi + '/v2/record/' + query.id
  const result = await $fetch(url,
    {
      method: 'DELETE',
    },
  )
  return result
})
