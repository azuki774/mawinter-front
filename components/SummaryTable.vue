<template>
  <div>
    <h2>{{ title }}</h2>
    <table class="table small bordered striped table-bordered w-100" style="table-layout: fixed;">
      <thead>
        <tr>
          <th scope="col" class="text-center" style="width: 5%">ID</th>
          <th scope="col" style="width: 15%">カテゴリ名</th>
          <th v-for="month in monthNames" :key="month" scope="col" class="text-center" style="width: 5.5%">
            {{ month }}
          </th>
          <th scope="col" class="text-center" style="width: 9%">合計</th>
        </tr>
      </thead>
      <tbody>
        <SummaryTableRow
          v-for="item in data"
          :key="item.category_id"
          :item="item"
        />
        <SummaryTableRow
          v-if="sumData && isLoaded"
          :item="sumData"
          :class-name="sumRowClass"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { SummaryOne } from '@/interfaces'

interface Props {
  title: string
  data?: SummaryOne[]
  sumData?: SummaryOne
  sumRowClass?: string
  isLoaded: boolean
}

defineProps<Props>()

const monthNames = ['4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
</script>
