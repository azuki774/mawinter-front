<script setup lang='ts'>
import type { HistoryAvailable } from '@/interfaces'

const availableYears = ref<string[]>([])
const latestYear = ref<string>()

onMounted(async () => {
  try {
    const availableData = await $fetch<HistoryAvailable>('/api/getAvailable')
    availableYears.value = availableData.fy || []
    if (availableYears.value.length > 0) {
      // 最新の年度（配列の最後）を取得
      latestYear.value = availableYears.value[availableYears.value.length - 1]
    }
  } catch (error) {
    // エラー時は現在の年度を使用
    const currentYear = new Date().getFullYear()
    latestYear.value = String(currentYear)
  }
})
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
