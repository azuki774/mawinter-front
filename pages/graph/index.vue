<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineController,
  BarController,
} from 'chart.js'
import { Chart } from 'vue-chartjs'
import type { SummaryOne } from '@/interfaces'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  LineController,
  BarController,
  Title,
  Tooltip,
  Legend,
)

// 現在の年度を計算（4月開始）
const getCurrentFiscalYear = (): number => {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1 // 0-based to 1-based

  // 4月以降なら現在年度、3月以前なら前年度
  return currentMonth >= 4 ? currentYear : currentYear - 1
}

const selectedYear = ref(getCurrentFiscalYear())
const summaryData = ref<SummaryOne[]>([])
const availableYears = ref<number[]>([])
const isLoading = ref(false)

// 利用可能年度を取得する
const fetchAvailableYears = async () => {
  try {
    const available = await $fetch<{ fy: string[] }>('/api/getAvailable')
    availableYears.value = available.fy.map(Number).sort((a, b) => b - a) // 降順ソート

    // 初期選択年度を利用可能年度の最新年に設定
    if (availableYears.value.length > 0) {
      selectedYear.value = availableYears.value[0]
    }
  }
  catch {
    // エラー時はフォールバック処理を実行
    // フォールバック：現在の年度から過去10年分
    availableYears.value = Array.from({ length: 10 }, (_, i) => getCurrentFiscalYear() - i)
  }
}

// APIからサマリーデータを取得
const fetchSummaryData = async () => {
  isLoading.value = true
  try {
    const data = await $fetch<SummaryOne[]>(`/api/summary?year=${selectedYear.value}`)
    summaryData.value = data || []
  }
  catch {
    summaryData.value = []
  }
  finally {
    isLoading.value = false
  }
}

// 月次支出推移データを生成（支出の棒グラフ + 収入の折れ線）
const monthlyExpenseData = computed(() => {
  if (!summaryData.value.length) return { labels: [], datasets: [] }

  // 支出カテゴリのみフィルタ（200番台から500番台まで）
  const expenseData = summaryData.value.filter(item =>
    item.category_id >= 200 && item.category_id <= 500,
  )

  // 収入カテゴリのみフィルタ（100番台）
  const incomeData = summaryData.value.filter(item =>
    item.category_id >= 100 && item.category_id <= 199,
  )

  // 支出カテゴリごとの棒グラフデータセットを作成
  const expenseDatasets = expenseData.map((item, index) => {
    const hue = (index * 360) / expenseData.length
    const color = `hsla(${hue}, 70%, 60%, 0.8)`

    return {
      label: item.category_name,
      type: 'bar' as const,
      backgroundColor: color,
      borderColor: color,
      borderWidth: 1,
      data: item.price.map(price => Math.abs(price)), // 支出は負の値なので絶対値に
    }
  })

  // 収入の合計を月別に計算
  const monthlyIncomeTotal = Array(12).fill(0)
  incomeData.forEach((item) => {
    item.price.forEach((price, index) => {
      monthlyIncomeTotal[index] += Math.abs(price) // 収入も絶対値で表示
    })
  })

  // 収入の折れ線データセットを作成
  const incomeDataset = {
    label: '収入合計',
    type: 'line' as const,
    borderColor: '#28a745',
    backgroundColor: 'transparent',
    borderWidth: 2,
    pointBackgroundColor: '#28a745',
    pointBorderColor: '#28a745',
    pointRadius: 3,
    pointBorderWidth: 1,
    data: monthlyIncomeTotal,
  }

  return {
    labels: ['4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月'],
    datasets: [...expenseDatasets, incomeDataset],
  }
})

// カテゴリ別支出データを生成（支出カテゴリのみ）
const categoryExpenseData = computed(() => {
  if (!summaryData.value.length) return { labels: [], datasets: [] }

  // 支出カテゴリのみフィルタ（200番台から500番台まで）
  const expenseData = summaryData.value.filter(item =>
    item.category_id >= 200 && item.category_id <= 500,
  )

  const labels = expenseData.map(item => item.category_name)
  const data = expenseData.map(item => Math.abs(item.total)) // 絶対値に変換

  // カテゴリ数に応じて色を生成
  const colors = expenseData.map((_, index) => {
    const hue = (index * 360) / expenseData.length
    return `hsla(${hue}, 70%, 60%, 0.6)`
  })

  return {
    labels,
    datasets: [
      {
        label: '年間支出額',
        backgroundColor: colors,
        data,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
  scales: {
    x: {
      stacked: true,
    },
    y: {
      type: 'linear' as const,
      display: true,
      position: 'left' as const,
      stacked: true,
      beginAtZero: true,
      title: {
        display: true,
        text: '金額 (円)',
      },
    },
  },
}

const categoryChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
}

// SSR対応：初期データを setup 内で取得
await fetchAvailableYears()
await fetchSummaryData()

// 年度変更時にデータを再取得
watch(selectedYear, () => {
  fetchSummaryData()
})
</script>

<template>
  <section>
    <h1>グラフ表示</h1>

    <div class="container-sm">
      <!-- 年度選択 -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-center align-items-center">
            <label for="yearSelect" class="form-label me-3">年度:</label>
            <select
              id="yearSelect"
              v-model="selectedYear"
              class="form-select w-auto"
              :disabled="isLoading"
            >
              <option v-for="year in availableYears" :key="year" :value="year">
                {{ year }}年度
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- ローディング表示 -->
      <div v-if="isLoading" class="text-center mb-4">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>データを読み込み中...</p>
      </div>

      <!-- グラフ表示 -->
      <div v-else class="row">
        <div class="col-12 mb-5">
          <h2>月次支出推移 ({{ selectedYear }}年度)</h2>
          <div style="height: 400px">
            <ClientOnly>
              <Chart type="bar" :data="monthlyExpenseData" :options="chartOptions" />
            </ClientOnly>
          </div>
        </div>

        <div class="col-12 mb-5">
          <h2>カテゴリ別支出 ({{ selectedYear }}年度)</h2>
          <div style="height: 400px">
            <ClientOnly>
              <Chart type="bar" :data="categoryExpenseData" :options="categoryChartOptions" />
            </ClientOnly>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
h1, h2 {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}
</style>
