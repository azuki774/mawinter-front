<script setup lang='ts'>

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

.search_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

</style>
