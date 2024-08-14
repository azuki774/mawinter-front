<script setup lang="ts">
import type { SummaryOne } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const summaryList = ref<SummaryOne[]>()
const asyncData = await useFetch(
  "/api/summary",
  {
    key: `/api/summary`,
    transform: (data: SummaryOne[]): SummaryOne[] => {
      let retArray: SummaryOne[] = [];
      for (let d of data) {
        if (d.category_id == 210) {
          retArray.push(d)
        }
      }
      return retArray
    }
  }
);

const data = asyncData.data.value as SummaryOne[];
summaryList.value = data

</script>

<template>
  <section>
    <table class="income_table">
      <thead>
        <tr>
          <th>ID</th>
          <th>カテゴリ名</th>
          <th>4月</th>
          <th>5月</th>
          <th>6月</th>
          <th>7月</th>
          <th>8月</th>
          <th>9月</th>
          <th>10月</th>
          <th>11月</th>
          <th>12月</th>
          <th>1月</th>
          <th>2月</th>
          <th>3月</th>
          <th>合計</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="summary in summaryList">
          <td>{{ summary.category_id }}</td>
          <td>{{ summary.category_name }}</td>
          <td>{{ summary.price[0] }}</td>
          <td>{{ summary.price[1] }}</td>
          <td>{{ summary.price[2] }}</td>
          <td>{{ summary.price[3] }}</td>
          <td>{{ summary.price[4] }}</td>
          <td>{{ summary.price[5] }}</td>
          <td>{{ summary.price[6] }}</td>
          <td>{{ summary.price[7] }}</td>
          <td>{{ summary.price[8] }}</td>
          <td>{{ summary.price[9] }}</td>
          <td>{{ summary.price[10] }}</td>
          <td>{{ summary.price[11] }}</td>
          <td>{{ summary.total }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
