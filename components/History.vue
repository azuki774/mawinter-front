<script setup lang="ts">
import type { Record } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const recordList = ref<Record[]>()
const asyncData = await useAsyncData(
  `history`,
  (): Promise<any> => {
    const url = config.public.mawinterApi + "/v2/record";
    const response = $fetch(url);
    return response;
  }
);

const data = asyncData.data.value as Record[];

// fetchデータを整形
for (let d of data) {
  d.datetime = d.datetime.slice(0, 19); // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
}

recordList.value = data

</script>

<template>
  <section>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>カテゴリ名</th>
          <th>金額</th>
          <th>日付</th>
          <th>メモ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in recordList">
          <td>{{ record.id }}</td>
          <td>{{ record.category_name }}</td>
          <td>{{ record.price }}</td>
          <td>{{ record.datetime }}</td>
          <td>{{ record.memo }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
