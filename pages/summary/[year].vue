<script setup lang='ts'>
import type { SummaryOne, HistoryAvailable } from '@/interfaces'

const { categorizeData, calculateSum, calculateNetSum } = useSummaryData()
const router = useRouter()
const route = useRoute()

const currentYear = route.params.year as string
const isLoading = ref(true)
const isError = ref(false)

const incomeList = ref<SummaryOne[]>([])
const outgoingList = ref<SummaryOne[]>([])
const investList = ref<SummaryOne[]>([])
const incomeSumList = ref<SummaryOne>()
const outgoingSumList = ref<SummaryOne>()
const investSumList = ref<SummaryOne>()
const allSumList = ref<SummaryOne>()
const allSumWithoutInvestList = ref<SummaryOne>()

const fetchSummary = async () => {
  try {
    isLoading.value = true
    isError.value = false
    const data = await $fetch<SummaryOne[]>(`/api/summary?year=${currentYear}`)

    if (data) {
      const { income, outgoing, invest } = categorizeData(data)

      incomeList.value = income
      outgoingList.value = outgoing
      investList.value = invest

      incomeSumList.value = calculateSum(income, '収入合計')
      outgoingSumList.value = calculateSum(outgoing, '支出合計')
      investSumList.value = calculateSum(invest, '投資合計')

      allSumList.value = calculateNetSum(
        incomeSumList.value,
        outgoingSumList.value,
        investSumList.value,
        true,
      )

      allSumWithoutInvestList.value = calculateNetSum(
        incomeSumList.value,
        outgoingSumList.value,
        investSumList.value,
        false,
      )
    }
  }
  catch {
    isError.value = true
  }
  finally {
    isLoading.value = false
  }
}

const availableYears = ref<string[]>([])
const selectedYear = ref<string>(currentYear)

const handleYearChange = (newYear: string) => {
  if (newYear !== currentYear) {
    router.push(`/summary/${newYear}`)
  }
}

onMounted(async () => {
  try {
    const availableData = await $fetch<HistoryAvailable>('/api/getAvailable')
    availableYears.value = availableData.fy || []
    selectedYear.value = currentYear
    await fetchSummary()
  }
  catch {
    isError.value = true
    isLoading.value = false
  }
})

watch(selectedYear, handleYearChange)

</script>

<template>
  <div class="container-fluid" style="padding-left: 8rem; padding-right: 8rem;">
    <h1>サマリー表示</h1>
    <NuxtLink to="/">トップに戻る</NuxtLink>

    <div class="col-2 mb-2">
      <label for="dropdown" class="d-block">取得年度:</label>
      <select id="dropdown" v-model="selectedYear" :disabled="isLoading">
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </div>

    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="isError" class="alert alert-danger" role="alert">
      データの取得に失敗しました。
    </div>

    <template v-else>

      <div>
        <h2>合計</h2>
        <table class="table small bordered striped table-bordered w-100" style="table-layout: fixed;">
          <thead>
            <tr>
              <th scope="col" class="text-center" style="width: 5%">ID</th>
              <th scope="col" style="width: 15%">カテゴリ名</th>
              <th scope="col" class="text-center" style="width: 5.5%">4月</th>
              <th scope="col" class="text-center" style="width: 5.5%">5月</th>
              <th scope="col" class="text-center" style="width: 5.5%">6月</th>
              <th scope="col" class="text-center" style="width: 5.5%">7月</th>
              <th scope="col" class="text-center" style="width: 5.5%">8月</th>
              <th scope="col" class="text-center" style="width: 5.5%">9月</th>
              <th scope="col" class="text-center" style="width: 5.5%">10月</th>
              <th scope="col" class="text-center" style="width: 5.5%">11月</th>
              <th scope="col" class="text-center" style="width: 5.5%">12月</th>
              <th scope="col" class="text-center" style="width: 5.5%">1月</th>
              <th scope="col" class="text-center" style="width: 5.5%">2月</th>
              <th scope="col" class="text-center" style="width: 5.5%">3月</th>
              <th scope="col" class="text-center" style="width: 9%">合計</th>
            </tr>
          </thead>
          <tbody>
            <SummaryTableRow
              v-if="allSumList"
              :item="allSumList"
            />
            <SummaryTableRow
              v-if="allSumWithoutInvestList"
              :item="allSumWithoutInvestList"
              class-name="table-info"
            />
          </tbody>
        </table>
      </div>

      <SummaryTable
        title="収入"
        :data="incomeList"
        :sum-data="incomeSumList"
        sum-row-class="table-success"
        :is-loaded="!isLoading"
      />

      <SummaryTable
        title="支出"
        :data="outgoingList"
        :sum-data="outgoingSumList"
        sum-row-class="table-danger"
        :is-loaded="!isLoading"
      />

      <SummaryTable
        title="投資"
        :data="investList"
        :sum-data="investSumList"
        sum-row-class="table-warning"
        :is-loaded="!isLoading"
      />
    </template>
  </div>
</template>
