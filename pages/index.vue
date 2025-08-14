<script setup lang='ts'>
import type { HistoryAvailable } from '@/interfaces'

const availableYears = ref<string[]>([])
const latestYear = ref<string>()

// SSR対応：サーバーサイドでもデータを取得
try {
  const availableData = await $fetch<HistoryAvailable>('/api/getAvailable')
  availableYears.value = availableData.fy || []
  if (availableYears.value.length > 0) {
    latestYear.value = availableYears.value[availableYears.value.length - 1]
  }
}
catch {
  const currentYear = new Date().getFullYear()
  latestYear.value = String(currentYear)
}
</script>

<template>
  <section>
  <h1>mawinter-front</h1>
    <h2>登録</h2>
    <PostRecord />

    <div class='graph_link'>
      <NuxtLink to="/graph">
        グラフ表示
      </NuxtLink>
    </div>

    <div class='summary_link'>
      <NuxtLink v-if="latestYear" :to="`/summary/${latestYear}`">
        サマリー表示
      </NuxtLink>
    </div>

    <div class="container-sm">
      <SearchHistory />
    </div>

  </section>
</template>

<style lang='css'>
h2 {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.graph_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.summary_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  margin-top: 1rem;
}

.search_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

</style>
