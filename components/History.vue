<script setup lang="ts">
import type { Record } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const recordList = ref<Record[]>()
const asyncData = await useAsyncData(
  `records`,
  (): Promise<any> => {
    const url = config.public.mawinterApi + "/v2/records";
    console.log(url)
    const response = $fetch(url);
    return response;
  }
);

const data = asyncData.data.value as Record[];
recordList.value = data
console.log(data)

</script>

<template>
  <section>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>金額</th>
          <th>日付</th>
          <th>メモ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in recordList">
          <td>{{ record.id }}</td>
          <td>{{ record.price }}</td>
          <td>{{ record.date }}</td>
          <td>{{ record.memo }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
