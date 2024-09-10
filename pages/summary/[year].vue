<script setup lang='ts'>
import type { SummaryOne } from '@/interfaces'
const incomeList = ref<SummaryOne[]>()
const incomeSumList = ref<SummaryOne>()
const outgoingList = ref<SummaryOne[]>()
const outgoingSumList = ref<SummaryOne>()
const investList = ref<SummaryOne[]>()
const investSumList = ref<SummaryOne>()
const AllSumList = ref<SummaryOne>() // 合計フィールド
const AllSumWithoutInvestList = ref<SummaryOne>() // 合計（投資除く）フィールド

let fetched: boolean // api fetch 出来ていたら true にする（表示制御用）

const route = useRoute()
const year = route.params.year
const asyncData = await useFetch(
  '/api/summary' + '?year=' + year, // webサーバ内ではクエリパラメータで渡す
  {
    key: `/api/summary`,
    transform: (data: SummaryOne[]): SummaryOne[][] => {
      const incomeArray: SummaryOne[] = []
      const outgoingArray: SummaryOne[] = []
      const investArray: SummaryOne[] = []
      for (const d of data) {
        if ([100, 101, 110].includes(d.category_id)) {
          incomeArray.push(d)
        }
        if ([200, 210, 220, 221, 222, 230, 231, 240, 250, 251, 260, 270, 280, 300, 400, 500].includes(d.category_id)) {
          outgoingArray.push(d)
        }
        if ([700, 701].includes(d.category_id)) {
          investArray.push(d)
        }
      }
      const retArray: SummaryOne[][] = [incomeArray, outgoingArray, investArray]
      return retArray
    },
  },
)

if (asyncData.data.value != undefined) {
  const incomeData = asyncData.data.value[0] as SummaryOne[]
  const outgoingData = asyncData.data.value[1] as SummaryOne[]
  const investData = asyncData.data.value[2] as SummaryOne[]
  incomeList.value = incomeData
  outgoingList.value = outgoingData
  investList.value = investData

  // sum の計算(income)
  const incomeSumData: SummaryOne = {
    category_id: 999,
    category_name: '収入合計',
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0,
  }

  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0
    let totalsum: number = 0
    for (const d of incomeData) {
      sum += d.price[i]
      totalsum += d.price[i]
    }
    incomeSumData.price[i] = sum
    incomeSumData.total += totalsum
  }
  incomeSumList.value = incomeSumData

  // sum の計算(outgoing)
  const outgoingSumData: SummaryOne = {
    category_id: 999,
    category_name: '支出合計',
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0,
  }
  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0
    let totalsum: number = 0
    for (const d of outgoingData) {
      sum += d.price[i]
      totalsum += d.price[i]
    }
    outgoingSumData.price[i] = sum
    outgoingSumData.total += totalsum
  }
  outgoingSumList.value = outgoingSumData

  // sum の計算(invest)
  const investSumData: SummaryOne = {
    category_id: 999,
    category_name: '投資合計',
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0,
  }

  for (let i: number = 0; i < 12; i++) {
    let sum: number = 0
    let totalsum: number = 0
    for (const d of investData) {
      sum += d.price[i]
      totalsum += d.price[i]
    }
    investSumData.price[i] = sum
    investSumData.total += totalsum
  }
  investSumList.value = investSumData

  // 合計テーブル用の計算
  const AllSumData: SummaryOne = {
    category_id: 999,
    category_name: '合計',
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0,
  }

  for (let i: number = 0; i < 12; i++) {
    AllSumData.price[i] = incomeSumData.price[i] - outgoingSumData.price[i] - investSumData.price[i]
  }
  AllSumData.total = incomeSumData.total - outgoingSumData.total - investSumData.total
  AllSumList.value = AllSumData

  const AllSumWithoutInvestData: SummaryOne = {
    category_id: 999,
    category_name: '合計（投資除く）',
    price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    total: 0,
  }

  for (let i: number = 0; i < 12; i++) {
    AllSumWithoutInvestData.price[i] = incomeSumData.price[i] - outgoingSumData.price[i]
  }
  AllSumWithoutInvestData.total = incomeSumData.total - outgoingSumData.total - investSumData.total
  AllSumWithoutInvestList.value = AllSumWithoutInvestData

  fetched = true // データ取得後のフラグを立てる
}

</script>

<template>
  <div class='container'>
  <h1>サマリー表示</h1>
    <a href='../'>トップに戻る</a>

    <h2>合計</h2>
    <table class='table small bordered striped table-bordered'>
      <thead>
        <tr>
          <th scope='col' style='width: 3%'>ID</th>
          <th scope='col' style='width: 10%'>カテゴリ名</th>
          <th scope='col' style='width: 5%'>4月</th>
          <th scope='col' style='width: 5%'>5月</th>
          <th scope='col' style='width: 5%'>6月</th>
          <th scope='col' style='width: 5%'>7月</th>
          <th scope='col' style='width: 5%'>8月</th>
          <th scope='col' style='width: 5%'>9月</th>
          <th scope='col' style='width: 5%'>10月</th>
          <th scope='col' style='width: 5%'>11月</th>
          <th scope='col' style='width: 5%'>12月</th>
          <th scope='col' style='width: 5%'>1月</th>
          <th scope='col' style='width: 5%'>2月</th>
          <th scope='col' style='width: 5%'>3月</th>
          <th scope='col' style='width: 7%'>合計</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if='fetched'>
          <td>{{ AllSumList?.category_id }}</td>
          <td>{{ AllSumList?.category_name }}</td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumList?.total }}</div>
          </td>
        </tr>
        <tr v-if='fetched' class='table-info'>
          <td>{{ AllSumWithoutInvestList?.category_id }}</td>
          <td>{{ AllSumWithoutInvestList?.category_name }}</td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ AllSumWithoutInvestList?.total }}</div>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>収入</h2>
    <table class='table small bordered striped table-bordered'>
      <thead>
        <tr>
          <th scope='col' style='width: 3%'>ID</th>
          <th scope='col' style='width: 10%'>カテゴリ名</th>
          <th scope='col' style='width: 5%'>4月</th>
          <th scope='col' style='width: 5%'>5月</th>
          <th scope='col' style='width: 5%'>6月</th>
          <th scope='col' style='width: 5%'>7月</th>
          <th scope='col' style='width: 5%'>8月</th>
          <th scope='col' style='width: 5%'>9月</th>
          <th scope='col' style='width: 5%'>10月</th>
          <th scope='col' style='width: 5%'>11月</th>
          <th scope='col' style='width: 5%'>12月</th>
          <th scope='col' style='width: 5%'>1月</th>
          <th scope='col' style='width: 5%'>2月</th>
          <th scope='col' style='width: 5%'>3月</th>
          <th scope='col' style='width: 7%'>合計</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for='income in incomeList' :key=income.id>
          <td>{{ income.category_id }}</td>
          <td>{{ income.category_name }}</td>
          <td>
            <div class='text-end'>{{ income.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ income.total }}</div>
          </td>
        </tr>
        <tr v-if='fetched' class='table-success'>
          <td>{{ incomeSumList?.category_id }}</td>
          <td>{{ incomeSumList?.category_name }}</td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ incomeSumList?.total }}</div>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>支出</h2>
    <table class='table small bordered striped table-bordered'>
      <thead>
        <tr>
          <th scope='col' style='width: 3%'>ID</th>
          <th scope='col' style='width: 10%'>カテゴリ名</th>
          <th scope='col' style='width: 5%'>4月</th>
          <th scope='col' style='width: 5%'>5月</th>
          <th scope='col' style='width: 5%'>6月</th>
          <th scope='col' style='width: 5%'>7月</th>
          <th scope='col' style='width: 5%'>8月</th>
          <th scope='col' style='width: 5%'>9月</th>
          <th scope='col' style='width: 5%'>10月</th>
          <th scope='col' style='width: 5%'>11月</th>
          <th scope='col' style='width: 5%'>12月</th>
          <th scope='col' style='width: 5%'>1月</th>
          <th scope='col' style='width: 5%'>2月</th>
          <th scope='col' style='width: 5%'>3月</th>
          <th scope='col' style='width: 7%'>合計</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for='outgoing in outgoingList' :key=outgoing.id>
          <td>{{ outgoing.category_id }}</td>
          <td>{{ outgoing.category_name }}</td>
          <td>
            <div class='text-end'>{{ outgoing.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoing.total }}</div>
          </td>
        </tr>
        <tr v-if='fetched' class='table-danger'>
          <td>{{ outgoingSumList?.category_id }}</td>
          <td>{{ outgoingSumList?.category_name }}</td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ outgoingSumList?.total }}</div>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>投資</h2>
    <table class='table small bordered striped table-bordered'>
      <thead>
        <tr>
          <th scope='col' style='width: 3%'>ID</th>
          <th scope='col' style='width: 10%'>カテゴリ名</th>
          <th scope='col' style='width: 5%'>4月</th>
          <th scope='col' style='width: 5%'>5月</th>
          <th scope='col' style='width: 5%'>6月</th>
          <th scope='col' style='width: 5%'>7月</th>
          <th scope='col' style='width: 5%'>8月</th>
          <th scope='col' style='width: 5%'>9月</th>
          <th scope='col' style='width: 5%'>10月</th>
          <th scope='col' style='width: 5%'>11月</th>
          <th scope='col' style='width: 5%'>12月</th>
          <th scope='col' style='width: 5%'>1月</th>
          <th scope='col' style='width: 5%'>2月</th>
          <th scope='col' style='width: 5%'>3月</th>
          <th scope='col' style='width: 7%'>合計</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for='invest in investList' :key=invest.id>
          <td>{{ invest.category_id }}</td>
          <td>{{ invest.category_name }}</td>
          <td>
            <div class='text-end'>{{ invest.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ invest.total }}</div>
          </td>
        </tr>
        <tr v-if='fetched' class='table-warning'>
          <td>{{ investSumList?.category_id }}</td>
          <td>{{ investSumList?.category_name }}</td>
          <td>
            <div class='text-end'>{{ investSumList?.price[0] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[1] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[2] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[3] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[4] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[5] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[6] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[7] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[8] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[9] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[10] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.price[11] }}</div>
          </td>
          <td>
            <div class='text-end'>{{ investSumList?.total }}</div>
          </td>
        </tr>
        </tbody>
    </table>

  </div>
</template>
