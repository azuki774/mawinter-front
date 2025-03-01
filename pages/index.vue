<script setup lang='ts'>
const today = new Date()
const thisYear = today.getFullYear()
const thisMonth = today.getMonth()

// year -> FY変換: 1月から3月なら年を1減らす.. 2025/03 -> FY2024
let thisFY = thisYear
if (thisMonth <= 3) {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  thisFY -= 1
}

</script>

<template>
  <section>
  <h1>mawinter-front</h1>
    <h2>登録</h2>
    <PostRecord />

    <div class='summary_link'>
      <NuxtLink v-bind:to="{name: 'summary-year', params: {year: thisFY}}">
        サマリー表示
      </NuxtLink>
    </div>

    <div class='search_link'>
      <NuxtLink v-bind:to="{name: 'search'}">
        履歴検索
      </NuxtLink>
    </div>

    <h2>直近履歴</h2>
    <ShowHistory />

  </section>
</template>

<style lang='css'>
h2 {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.summary_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.search_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

</style>
