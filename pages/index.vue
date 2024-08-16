<template>
  <h1>mawinter-front</h1>
  <section>
    <p text-alignment="center">
      <h2>登録</h2>
      <PostRecord />
    </p>

    <p text-alignment="center">
      <div class="summary_link">
        <NuxtLink to='/summary'>サマリー表示</NuxtLink>
      </div>
    </p>

    <p text-alignment="center">
      <h2>直近履歴</h2>
      <History />
    </p>
  </section>
</template>

<style lang="css">
.summary_link {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}
</style>
