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

    <b-h level="2">合計</b-h>
    <b-table small bordered striped class="all_table">
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">ID</b-th>
          <b-th style="width: 10%">カテゴリ名</b-th>
          <b-th style="width: 5%">4月</b-th>
          <b-th style="width: 5%">5月</b-th>
          <b-th style="width: 5%">6月</b-th>
          <b-th style="width: 5%">7月</b-th>
          <b-th style="width: 5%">8月</b-th>
          <b-th style="width: 5%">9月</b-th>
          <b-th style="width: 5%">10月</b-th>
          <b-th style="width: 5%">11月</b-th>
          <b-th style="width: 5%">12月</b-th>
          <b-th style="width: 5%">1月</b-th>
          <b-th style="width: 5%">2月</b-th>
          <b-th style="width: 5%">3月</b-th>
          <b-th style="width: 5%">合計</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-if="fetched">
          <b-td>{{ AllSumList.category_id }}</b-td>
          <b-td>{{ AllSumList.category_name }}</b-td>
          <b-td><b-div float="end">{{ AllSumList.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumList.total }}</b-div></b-td>
        </b-tr>
        <b-tr v-if="fetched">
          <b-td>{{ AllSumWithoutInvestList.category_id }}</b-td>
          <b-td>{{ AllSumWithoutInvestList.category_name }}</b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ AllSumWithoutInvestList.total }}</b-div></b-td>
        </b-tr>
      </b-tbody>
    </b-table>

    <b-h level="2">収入</b-h>
    <b-table small bordered striped class="income_table">
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">ID</b-th>
          <b-th style="width: 10%">カテゴリ名</b-th>
          <b-th style="width: 5%">4月</b-th>
          <b-th style="width: 5%">5月</b-th>
          <b-th style="width: 5%">6月</b-th>
          <b-th style="width: 5%">7月</b-th>
          <b-th style="width: 5%">8月</b-th>
          <b-th style="width: 5%">9月</b-th>
          <b-th style="width: 5%">10月</b-th>
          <b-th style="width: 5%">11月</b-th>
          <b-th style="width: 5%">12月</b-th>
          <b-th style="width: 5%">1月</b-th>
          <b-th style="width: 5%">2月</b-th>
          <b-th style="width: 5%">3月</b-th>
          <b-th style="width: 5%">合計</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-for="income in incomeList">
          <b-td>{{ income.category_id }}</b-td>
          <b-td>{{ income.category_name }}</b-td>
          <b-td><b-div float="end">{{ income.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ income.total }}</b-div></b-td>
        </b-tr>
        <b-tr v-if="fetched" theme="success">
          <b-td>{{ incomeSumList.category_id }}</b-td>
          <b-td>{{ incomeSumList.category_name }}</b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ incomeSumList.total }}</b-div></b-td>
        </b-tr>
      </b-tbody>
    </b-table>

    <b-h level="2">支出</b-h>
    <b-table small bordered striped class="outgoing_table">
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">ID</b-th>
          <b-th style="width: 10%">カテゴリ名</b-th>
          <b-th style="width: 5%">4月</b-th>
          <b-th style="width: 5%">5月</b-th>
          <b-th style="width: 5%">6月</b-th>
          <b-th style="width: 5%">7月</b-th>
          <b-th style="width: 5%">8月</b-th>
          <b-th style="width: 5%">9月</b-th>
          <b-th style="width: 5%">10月</b-th>
          <b-th style="width: 5%">11月</b-th>
          <b-th style="width: 5%">12月</b-th>
          <b-th style="width: 5%">1月</b-th>
          <b-th style="width: 5%">2月</b-th>
          <b-th style="width: 5%">3月</b-th>
          <b-th style="width: 5%">合計</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-for="outgoing in outgoingList">
          <b-td>{{ outgoing.category_id }}</b-td>
          <b-td>{{ outgoing.category_name }}</b-td>
          <b-td><b-div float="end">{{ outgoing.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoing.total }}</b-div></b-td>
        </b-tr>
        <b-tr v-if="fetched" theme="danger">
          <b-td>{{ outgoingSumList.category_id }}</b-td>
          <b-td>{{ outgoingSumList.category_name }}</b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ outgoingSumList.total }}</b-div></b-td>
        </b-tr>
      </b-tbody>
    </b-table>

    <b-table small bordered striped class="invest_table">
      <b-thead>
        <b-tr>
          <b-th style="width: 5%">ID</b-th>
          <b-th style="width: 10%">カテゴリ名</b-th>
          <b-th style="width: 5%">4月</b-th>
          <b-th style="width: 5%">5月</b-th>
          <b-th style="width: 5%">6月</b-th>
          <b-th style="width: 5%">7月</b-th>
          <b-th style="width: 5%">8月</b-th>
          <b-th style="width: 5%">9月</b-th>
          <b-th style="width: 5%">10月</b-th>
          <b-th style="width: 5%">11月</b-th>
          <b-th style="width: 5%">12月</b-th>
          <b-th style="width: 5%">1月</b-th>
          <b-th style="width: 5%">2月</b-th>
          <b-th style="width: 5%">3月</b-th>
          <b-th style="width: 5%">合計</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-for="invest in investList">
          <b-td>{{ invest.category_id }}</b-td>
          <b-td>{{ invest.category_name }}</b-td>
          <b-td><b-div float="end">{{ invest.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ invest.total }}</b-div></b-td>
        </b-tr>
        <b-tr v-if="fetched" theme="warning">
          <b-td>{{ investSumList.category_id }}</b-td>
          <b-td>{{ investSumList.category_name }}</b-td>
          <b-td><b-div float="end">{{ investSumList.price[0] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[1] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[2] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[3] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[4] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[5] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[6] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[7] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[8] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[9] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[10] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.price[11] }}</b-div></b-td>
          <b-td><b-div float="end">{{ investSumList.total }}</b-div></b-td>
        </b-tr>
      </b-tbody>
    </b-table>

  </container>
</template>
