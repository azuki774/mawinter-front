// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  routeRules: {
    "/": { ssr: false },
  },
  runtimeConfig: {
    public: { // 外部から取得するにはpublic が必要
      mawinterApi: "http://mawinter-api", // .env の NUXT_PUBLIC_API_BASE_ENDPOINT から取得
    }
  }
})
