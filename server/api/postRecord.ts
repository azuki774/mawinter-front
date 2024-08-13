export default defineEventHandler ( async (event) => {
    const config = useRuntimeConfig()
    const query = getQuery(event)
    const url = "http://172.19.250.172:8080/v2/records" // TODO
    const result = await $fetch(url)
    return result
})
