<script setup lang="ts">
import type { SummaryOne } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const incomeList = ref<SummaryOne[]>()
const incomeSumList = ref<SummaryOne>()
const outgoingList = ref<SummaryOne[]>()
const outgoingSumList = ref<SummaryOne>()
const investList = ref<SummaryOne[]>()
const investSumList = ref<SummaryOne>()
const AllSumList = ref<SummaryOne>() // 合計フィールド
const AllSumWithoutInvestList = ref<SummaryOne>() // 合計（投資除く）フィールド

let fetched: boolean // api fetch 出来ていたら true にする（表示制御用）
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

  // sum の計算(income)
  let incomeSumData: SummaryOne = {
    category_id: 999,
    category_name: "収入合計",
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0
  };

  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0;
    let totalsum: number = 0;
    for (let d of incomeData) {
      sum += d.price[i];
      totalsum += d.price[i];
    }
    incomeSumData.price[i] = sum;
    incomeSumData.total += totalsum;
  }
  incomeSumList.value = incomeSumData

  // sum の計算(outgoing)
  let outgoingSumData: SummaryOne = {
    category_id: 999,
    category_name: "支出合計",
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0
  };
  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0;
    let totalsum: number = 0;
    for (let d of outgoingData) {
      sum += d.price[i];
      totalsum += d.price[i];
    }
    outgoingSumData.price[i] = sum;
    outgoingSumData.total += totalsum;
  }
  outgoingSumList.value = outgoingSumData

  // sum の計算(invest)
  let investSumData: SummaryOne = {
    category_id: 999,
    category_name: "投資合計",
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0
  };

  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0;
    let totalsum: number = 0;
    for (let d of investData) {
      sum += d.price[i];
      totalsum += d.price[i];
    }
    investSumData.price[i] = sum;
    investSumData.total += totalsum;
  }
  investSumList.value = investSumData

  // 合計テーブル用の計算
  let AllSumData: SummaryOne = {
    category_id: 999,
    category_name: "合計",
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0
  };

  for (let i: number = 0; i < 12; i++) {
    AllSumData.price[i] = incomeSumData.price[i] - outgoingSumData.price[i] - investSumData.price[i];
  }
  AllSumData.total = incomeSumData.total - outgoingSumData.total - investSumData.total;
  AllSumList.value = AllSumData

  let AllSumWithoutInvestData: SummaryOne = {
    category_id: 999,
    category_name: "合計（投資除く）",
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0
  };

  for (let i: number = 0; i < 12; i++) {
    AllSumWithoutInvestData.price[i] = incomeSumData.price[i] - outgoingSumData.price[i];
  }
  AllSumWithoutInvestData.total = incomeSumData.total - outgoingSumData.total - investSumData.total;
  AllSumWithoutInvestList.value = AllSumWithoutInvestData

  fetched = true // データ取得後のフラグを立てる
}

</script>

<template>
  <NuxtLink to='/'>トップに戻る</NuxtLink>
  <section>
    <h2>合計</h2>
    <table class="all_table">
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
        <tr v-if="fetched">
          <td>{{ AllSumList.category_id }}</td>
          <td>{{ AllSumList.category_name }}</td>
          <td>{{ AllSumList.price[0] }}</td>
          <td>{{ AllSumList.price[1] }}</td>
          <td>{{ AllSumList.price[2] }}</td>
          <td>{{ AllSumList.price[3] }}</td>
          <td>{{ AllSumList.price[4] }}</td>
          <td>{{ AllSumList.price[5] }}</td>
          <td>{{ AllSumList.price[6] }}</td>
          <td>{{ AllSumList.price[7] }}</td>
          <td>{{ AllSumList.price[8] }}</td>
          <td>{{ AllSumList.price[9] }}</td>
          <td>{{ AllSumList.price[10] }}</td>
          <td>{{ AllSumList.price[11] }}</td>
          <td>{{ AllSumList.total }}</td>
        </tr>
        <tr v-if="fetched">
          <td>{{ AllSumWithoutInvestList.category_id }}</td>
          <td>{{ AllSumWithoutInvestList.category_name }}</td>
          <td>{{ AllSumWithoutInvestList.price[0] }}</td>
          <td>{{ AllSumWithoutInvestList.price[1] }}</td>
          <td>{{ AllSumWithoutInvestList.price[2] }}</td>
          <td>{{ AllSumWithoutInvestList.price[3] }}</td>
          <td>{{ AllSumWithoutInvestList.price[4] }}</td>
          <td>{{ AllSumWithoutInvestList.price[5] }}</td>
          <td>{{ AllSumWithoutInvestList.price[6] }}</td>
          <td>{{ AllSumWithoutInvestList.price[7] }}</td>
          <td>{{ AllSumWithoutInvestList.price[8] }}</td>
          <td>{{ AllSumWithoutInvestList.price[9] }}</td>
          <td>{{ AllSumWithoutInvestList.price[10] }}</td>
          <td>{{ AllSumWithoutInvestList.price[11] }}</td>
          <td>{{ AllSumWithoutInvestList.total }}</td>
        </tr>
      </tbody>
    </table>

    <h2>収入</h2>
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
        <tr v-if="fetched">
          <td>{{ incomeSumList.category_id }}</td>
          <td>{{ incomeSumList.category_name }}</td>
          <td>{{ incomeSumList.price[0] }}</td>
          <td>{{ incomeSumList.price[1] }}</td>
          <td>{{ incomeSumList.price[2] }}</td>
          <td>{{ incomeSumList.price[3] }}</td>
          <td>{{ incomeSumList.price[4] }}</td>
          <td>{{ incomeSumList.price[5] }}</td>
          <td>{{ incomeSumList.price[6] }}</td>
          <td>{{ incomeSumList.price[7] }}</td>
          <td>{{ incomeSumList.price[8] }}</td>
          <td>{{ incomeSumList.price[9] }}</td>
          <td>{{ incomeSumList.price[10] }}</td>
          <td>{{ incomeSumList.price[11] }}</td>
          <td>{{ incomeSumList.total }}</td>
        </tr>
      </tbody>
    </table>

    <h2>支出</h2>
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
        <tr v-if="fetched">
          <td>{{ outgoingSumList.category_id }}</td>
          <td>{{ outgoingSumList.category_name }}</td>
          <td>{{ outgoingSumList.price[0] }}</td>
          <td>{{ outgoingSumList.price[1] }}</td>
          <td>{{ outgoingSumList.price[2] }}</td>
          <td>{{ outgoingSumList.price[3] }}</td>
          <td>{{ outgoingSumList.price[4] }}</td>
          <td>{{ outgoingSumList.price[5] }}</td>
          <td>{{ outgoingSumList.price[6] }}</td>
          <td>{{ outgoingSumList.price[7] }}</td>
          <td>{{ outgoingSumList.price[8] }}</td>
          <td>{{ outgoingSumList.price[9] }}</td>
          <td>{{ outgoingSumList.price[10] }}</td>
          <td>{{ outgoingSumList.price[11] }}</td>
          <td>{{ outgoingSumList.total }}</td>
        </tr>
      </tbody>
    </table>

    <h2>投資</h2>
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
        <tr v-if="fetched">
          <td>{{ investSumList.category_id }}</td>
          <td>{{ investSumList.category_name }}</td>
          <td>{{ investSumList.price[0] }}</td>
          <td>{{ investSumList.price[1] }}</td>
          <td>{{ investSumList.price[2] }}</td>
          <td>{{ investSumList.price[3] }}</td>
          <td>{{ investSumList.price[4] }}</td>
          <td>{{ investSumList.price[5] }}</td>
          <td>{{ investSumList.price[6] }}</td>
          <td>{{ investSumList.price[7] }}</td>
          <td>{{ investSumList.price[8] }}</td>
          <td>{{ investSumList.price[9] }}</td>
          <td>{{ investSumList.price[10] }}</td>
          <td>{{ investSumList.price[11] }}</td>
          <td>{{ investSumList.total }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
