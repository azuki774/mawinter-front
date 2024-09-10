<script setup lang='ts'>
const today = new Date()
const thisYear = today.getFullYear()
</script>

<template>
  <section>
  <h1>mawinter-front</h1>
    <h2>登録</h2>
    <PostRecord />

    <div class='summary_link'>
      <NuxtLink v-bind:to="{name: 'summary-year', params: {year: thisYear}}">
        サマリー表示
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
</style>
