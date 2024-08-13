export default defineEventHandler ( async (event) => {
    const config = useRuntimeConfig()
    const url = config.public.mawinterApi + "/v2/record"
    const result = await $fetch(url,
      {
          method: "GET",
      }
    )
    return result
})
