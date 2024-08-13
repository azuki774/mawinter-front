export default defineEventHandler ( async (event) => {
  const config = useRuntimeConfig()
  const url = config.public.mawinterApi + "/categories"
  const result = await $fetch(url,
    {
        method: "GET",
    }
  )
  return result
})
