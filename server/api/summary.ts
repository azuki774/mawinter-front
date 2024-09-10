export default defineEventHandler (async () => {
  const config = useRuntimeConfig()
  const url = config.public.mawinterApi + '/v2/record/summary/2024'
  const result = await $fetch(url,
    {
      method: 'GET',
    },
  )
  return result
})
