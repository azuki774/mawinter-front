<template>
  <h1>mawinter-front</h1>
  <section>
    <p text-alignment="center">
    <h2>登録</h2>
    <PostRecord />
    </p>

    <div class="summary_link">
      <a href="/summary">サマリー表示</a>
    </div>

    <p text-alignment="center">
    <h2>直近履歴</h2>
    <History />
    </p>
  </section>
</template>

<style lang="css">
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
