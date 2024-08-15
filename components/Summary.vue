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

  <container>
    <b-p text-alignment="center">
      <NuxtLink to='/'>トップに戻る</NuxtLink>
    </b-p>

    <b-p text-alignment="center">
      <b-h level="2">合計</b-h>
      <b-table class="all_table">
        <b-thead>
          <b-tr>
            <b-th>ID</b-th>
            <b-th>カテゴリ名</b-th>
            <b-th>4月</b-th>
            <b-th>5月</b-th>
            <b-th>6月</b-th>
            <b-th>7月</b-th>
            <b-th>8月</b-th>
            <b-th>9月</b-th>
            <b-th>10月</b-th>
            <b-th>11月</b-th>
            <b-th>12月</b-th>
            <b-th>1月</b-th>
            <b-th>2月</b-th>
            <b-th>3月</b-th>
            <b-th>合計</b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr v-if="fetched">
            <b-td>{{ AllSumList.category_id }}</b-td>
            <b-td>{{ AllSumList.category_name }}</b-td>
            <b-td>{{ AllSumList.price[0] }}</b-td>
            <b-td>{{ AllSumList.price[1] }}</b-td>
            <b-td>{{ AllSumList.price[2] }}</b-td>
            <b-td>{{ AllSumList.price[3] }}</b-td>
            <b-td>{{ AllSumList.price[4] }}</b-td>
            <b-td>{{ AllSumList.price[5] }}</b-td>
            <b-td>{{ AllSumList.price[6] }}</b-td>
            <b-td>{{ AllSumList.price[7] }}</b-td>
            <b-td>{{ AllSumList.price[8] }}</b-td>
            <b-td>{{ AllSumList.price[9] }}</b-td>
            <b-td>{{ AllSumList.price[10] }}</b-td>
            <b-td>{{ AllSumList.price[11] }}</b-td>
            <b-td>{{ AllSumList.total }}</b-td>
          </b-tr>
          <b-tr v-if="fetched">
            <b-td>{{ AllSumWithoutInvestList.category_id }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.category_name }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[0] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[1] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[2] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[3] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[4] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[5] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[6] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[7] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[8] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[9] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[10] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.price[11] }}</b-td>
            <b-td>{{ AllSumWithoutInvestList.total }}</b-td>
          </b-tr>
        </b-tbody>
      </b-table>
    </b-p>

    <b-p text-alignment="center">
      <b-h level="2">収入</b-h>
      <b-table class="income_table">
        <b-thead>
          <b-tr>
            <b-th>ID</b-th>
            <b-th>カテゴリ名</b-th>
            <b-th>4月</b-th>
            <b-th>5月</b-th>
            <b-th>6月</b-th>
            <b-th>7月</b-th>
            <b-th>8月</b-th>
            <b-th>9月</b-th>
            <b-th>10月</b-th>
            <b-th>11月</b-th>
            <b-th>12月</b-th>
            <b-th>1月</b-th>
            <b-th>2月</b-th>
            <b-th>3月</b-th>
            <b-th>合計</b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr v-for="income in incomeList">
            <b-td>{{ income.category_id }}</b-td>
            <b-td>{{ income.category_name }}</b-td>
            <b-td>{{ income.price[0] }}</b-td>
            <b-td>{{ income.price[1] }}</b-td>
            <b-td>{{ income.price[2] }}</b-td>
            <b-td>{{ income.price[3] }}</b-td>
            <b-td>{{ income.price[4] }}</b-td>
            <b-td>{{ income.price[5] }}</b-td>
            <b-td>{{ income.price[6] }}</b-td>
            <b-td>{{ income.price[7] }}</b-td>
            <b-td>{{ income.price[8] }}</b-td>
            <b-td>{{ income.price[9] }}</b-td>
            <b-td>{{ income.price[10] }}</b-td>
            <b-td>{{ income.price[11] }}</b-td>
            <b-td>{{ income.total }}</b-td>
          </b-tr>
          <b-tr v-if="fetched" theme="success">
            <b-td>{{ incomeSumList.category_id }}</b-td>
            <b-td>{{ incomeSumList.category_name }}</b-td>
            <b-td>{{ incomeSumList.price[0] }}</b-td>
            <b-td>{{ incomeSumList.price[1] }}</b-td>
            <b-td>{{ incomeSumList.price[2] }}</b-td>
            <b-td>{{ incomeSumList.price[3] }}</b-td>
            <b-td>{{ incomeSumList.price[4] }}</b-td>
            <b-td>{{ incomeSumList.price[5] }}</b-td>
            <b-td>{{ incomeSumList.price[6] }}</b-td>
            <b-td>{{ incomeSumList.price[7] }}</b-td>
            <b-td>{{ incomeSumList.price[8] }}</b-td>
            <b-td>{{ incomeSumList.price[9] }}</b-td>
            <b-td>{{ incomeSumList.price[10] }}</b-td>
            <b-td>{{ incomeSumList.price[11] }}</b-td>
            <b-td>{{ incomeSumList.total }}</b-td>
          </b-tr>
        </b-tbody>
      </b-table>
    </b-p>

    <b-p text-alignment="center">
      <b-h level="2">支出</b-h>
      <b-table class="outgoing_table">
        <b-thead>
          <b-tr>
            <b-th>ID</b-th>
            <b-th>カテゴリ名</b-th>
            <b-th>4月</b-th>
            <b-th>5月</b-th>
            <b-th>6月</b-th>
            <b-th>7月</b-th>
            <b-th>8月</b-th>
            <b-th>9月</b-th>
            <b-th>10月</b-th>
            <b-th>11月</b-th>
            <b-th>12月</b-th>
            <b-th>1月</b-th>
            <b-th>2月</b-th>
            <b-th>3月</b-th>
            <b-th>合計</b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr v-for="outgoing in outgoingList">
            <b-td>{{ outgoing.category_id }}</b-td>
            <b-td>{{ outgoing.category_name }}</b-td>
            <b-td>{{ outgoing.price[0] }}</b-td>
            <b-td>{{ outgoing.price[1] }}</b-td>
            <b-td>{{ outgoing.price[2] }}</b-td>
            <b-td>{{ outgoing.price[3] }}</b-td>
            <b-td>{{ outgoing.price[4] }}</b-td>
            <b-td>{{ outgoing.price[5] }}</b-td>
            <b-td>{{ outgoing.price[6] }}</b-td>
            <b-td>{{ outgoing.price[7] }}</b-td>
            <b-td>{{ outgoing.price[8] }}</b-td>
            <b-td>{{ outgoing.price[9] }}</b-td>
            <b-td>{{ outgoing.price[10] }}</b-td>
            <b-td>{{ outgoing.price[11] }}</b-td>
            <b-td>{{ outgoing.total }}</b-td>
          </b-tr>
          <b-tr v-if="fetched" theme="danger">
            <b-td>{{ outgoingSumList.category_id }}</b-td>
            <b-td>{{ outgoingSumList.category_name }}</b-td>
            <b-td>{{ outgoingSumList.price[0] }}</b-td>
            <b-td>{{ outgoingSumList.price[1] }}</b-td>
            <b-td>{{ outgoingSumList.price[2] }}</b-td>
            <b-td>{{ outgoingSumList.price[3] }}</b-td>
            <b-td>{{ outgoingSumList.price[4] }}</b-td>
            <b-td>{{ outgoingSumList.price[5] }}</b-td>
            <b-td>{{ outgoingSumList.price[6] }}</b-td>
            <b-td>{{ outgoingSumList.price[7] }}</b-td>
            <b-td>{{ outgoingSumList.price[8] }}</b-td>
            <b-td>{{ outgoingSumList.price[9] }}</b-td>
            <b-td>{{ outgoingSumList.price[10] }}</b-td>
            <b-td>{{ outgoingSumList.price[11] }}</b-td>
            <b-td>{{ outgoingSumList.total }}</b-td>
          </b-tr>
        </b-tbody>
      </b-table>
    </b-p>

    <b-p text-alignment="center">
      <b-h level="2">投資</b-h>
      <b-table class="invest_table">
        <b-thead>
          <b-tr>
            <b-th>ID</b-th>
            <b-th>カテゴリ名</b-th>
            <b-th>4月</b-th>
            <b-th>5月</b-th>
            <b-th>6月</b-th>
            <b-th>7月</b-th>
            <b-th>8月</b-th>
            <b-th>9月</b-th>
            <b-th>10月</b-th>
            <b-th>11月</b-th>
            <b-th>12月</b-th>
            <b-th>1月</b-th>
            <b-th>2月</b-th>
            <b-th>3月</b-th>
            <b-th>合計</b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr v-for="invest in investList">
            <b-td>{{ invest.category_id }}</b-td>
            <b-td>{{ invest.category_name }}</b-td>
            <b-td>{{ invest.price[0] }}</b-td>
            <b-td>{{ invest.price[1] }}</b-td>
            <b-td>{{ invest.price[2] }}</b-td>
            <b-td>{{ invest.price[3] }}</b-td>
            <b-td>{{ invest.price[4] }}</b-td>
            <b-td>{{ invest.price[5] }}</b-td>
            <b-td>{{ invest.price[6] }}</b-td>
            <b-td>{{ invest.price[7] }}</b-td>
            <b-td>{{ invest.price[8] }}</b-td>
            <b-td>{{ invest.price[9] }}</b-td>
            <b-td>{{ invest.price[10] }}</b-td>
            <b-td>{{ invest.price[11] }}</b-td>
            <b-td>{{ invest.total }}</b-td>
          </b-tr>
          <b-tr v-if="fetched" theme="warning">
            <b-td>{{ investSumList.category_id }}</b-td>
            <b-td>{{ investSumList.category_name }}</b-td>
            <b-td>{{ investSumList.price[0] }}</b-td>
            <b-td>{{ investSumList.price[1] }}</b-td>
            <b-td>{{ investSumList.price[2] }}</b-td>
            <b-td>{{ investSumList.price[3] }}</b-td>
            <b-td>{{ investSumList.price[4] }}</b-td>
            <b-td>{{ investSumList.price[5] }}</b-td>
            <b-td>{{ investSumList.price[6] }}</b-td>
            <b-td>{{ investSumList.price[7] }}</b-td>
            <b-td>{{ investSumList.price[8] }}</b-td>
            <b-td>{{ investSumList.price[9] }}</b-td>
            <b-td>{{ investSumList.price[10] }}</b-td>
            <b-td>{{ investSumList.price[11] }}</b-td>
            <b-td>{{ investSumList.total }}</b-td>
          </b-tr>
        </b-tbody>
      </b-table>
    </b-p>
  </container>
</template>
