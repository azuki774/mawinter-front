// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  devtools: { enabled: true },
  routeRules: {
    '/': { ssr: false },
  },
  runtimeConfig: {
    public: { // 外部から取得するにはpublic が必要
      mawinterApi: 'http://mawinter-api', // .env の NUXT_PUBLIC_MAWINTER_API から取得 (Nuxtが自動的にマッピング)
    },
  },
  modules: [
    '@nuxt/eslint',
  ],
})
