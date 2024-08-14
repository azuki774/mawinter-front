<script setup lang="ts">
import type { SummaryOne } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const incomeList = ref<SummaryOne[]>()
const outgoingList = ref<SummaryOne[]>()
const investList = ref<SummaryOne[]>()
const asyncData = await useFetch(
  "/api/summary",
  {
    key: `/api/summary`,
    transform: (data: SummaryOne[]): SummaryOne[][] => {
      let incomeArray: SummaryOne[] = [];
      let outgoingArray: SummaryOne[] = [];
      let investArray: SummaryOne[] = [];
      for (let d of data) {
        if ([100, 101, 110].includes(d.category_id)) {
          incomeArray.push(d)
        }
        if ([200, 210, 220, 221, 222, 230, 231, 240, 251, 260, 270, 280, 300, 400, 500].includes(d.category_id)) {
          outgoingArray.push(d)
        }
        if ([700, 701].includes(d.category_id)) {
          investArray.push(d)
        }
      }
      const retArray: SummaryOne[][] = [incomeArray, outgoingArray, investArray]
      return retArray
    }
  }
);

if (asyncData.data.value != undefined) {
  const incomeData = asyncData.data.value[0] as SummaryOne[];
  const outgoingData = asyncData.data.value[1] as SummaryOne[];
  const investData = asyncData.data.value[2] as SummaryOne[];
  incomeList.value = incomeData
  outgoingList.value = outgoingData
  investList.value = investData
}

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
        <tr v-for="income in incomeList">
          <td>{{ income.category_id }}</td>
          <td>{{ income.category_name }}</td>
          <td>{{ income.price[0] }}</td>
          <td>{{ income.price[1] }}</td>
          <td>{{ income.price[2] }}</td>
          <td>{{ income.price[3] }}</td>
          <td>{{ income.price[4] }}</td>
          <td>{{ income.price[5] }}</td>
          <td>{{ income.price[6] }}</td>
          <td>{{ income.price[7] }}</td>
          <td>{{ income.price[8] }}</td>
          <td>{{ income.price[9] }}</td>
          <td>{{ income.price[10] }}</td>
          <td>{{ income.price[11] }}</td>
          <td>{{ income.total }}</td>
        </tr>
      </tbody>
    </table>

    <table class="outgoing_table">
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
        <tr v-for="outgoing in outgoingList">
          <td>{{ outgoing.category_id }}</td>
          <td>{{ outgoing.category_name }}</td>
          <td>{{ outgoing.price[0] }}</td>
          <td>{{ outgoing.price[1] }}</td>
          <td>{{ outgoing.price[2] }}</td>
          <td>{{ outgoing.price[3] }}</td>
          <td>{{ outgoing.price[4] }}</td>
          <td>{{ outgoing.price[5] }}</td>
          <td>{{ outgoing.price[6] }}</td>
          <td>{{ outgoing.price[7] }}</td>
          <td>{{ outgoing.price[8] }}</td>
          <td>{{ outgoing.price[9] }}</td>
          <td>{{ outgoing.price[10] }}</td>
          <td>{{ outgoing.price[11] }}</td>
          <td>{{ outgoing.total }}</td>
        </tr>
      </tbody>
    </table>

    <table class="invest_table">
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
        <tr v-for="invest in investList">
          <td>{{ invest.category_id }}</td>
          <td>{{ invest.category_name }}</td>
          <td>{{ invest.price[0] }}</td>
          <td>{{ invest.price[1] }}</td>
          <td>{{ invest.price[2] }}</td>
          <td>{{ invest.price[3] }}</td>
          <td>{{ invest.price[4] }}</td>
          <td>{{ invest.price[5] }}</td>
          <td>{{ invest.price[6] }}</td>
          <td>{{ invest.price[7] }}</td>
          <td>{{ invest.price[8] }}</td>
          <td>{{ invest.price[9] }}</td>
          <td>{{ invest.price[10] }}</td>
          <td>{{ invest.price[11] }}</td>
          <td>{{ invest.total }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
