// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  css: ["bootstrap/dist/css/bootstrap.min.css"],
  devtools: { enabled: true },
  routeRules: {
    "/": { ssr: true },
  },
  runtimeConfig: {
    public: { // 外部から取得するにはpublic が必要
      mawinterApi: "http://mawinter-api", // .env の NUXT_PUBLIC_API_BASE_ENDPOINT から取得
    }
  },
  modules: [
    '@nuxt/eslint'
  ],
  
})
