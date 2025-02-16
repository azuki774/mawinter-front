<script setup lang='ts'>
import { ref } from 'vue'
import type { Record } from '@/interfaces'
import type { Header, Item } from 'vue3-easy-data-table'

const asyncData = await useFetch(
  '/api/getHistories?yyyymm=202502',
  {
    key: `/api/getHistories?yyyymm=202502`,
  },
)

const data = asyncData.data.value as Record[]

// fetchデータを整形
if (data != undefined) { // 取得済の場合のみ
  for (const d of data) {
    d.datetime = d.datetime.slice(0, 19) // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
  }
}

const headers = ref<Header[]>([
  { text: 'ID', value: 'id' },
  { text: 'カテゴリ名', value: 'category_name', sortable: true },
  { text: '利用日', value: 'datetime', sortable: true },
  { text: '登録元', value: 'from' },
  { text: '金額', value: 'price', sortable: true },
  { text: 'メモ', value: 'memo' },
])

const items = ref<Item[]>(data)

</script>

<template>
      <div class='row justify-content-center'>
      <h2>レコード</h2>
      <EasyDataTable :headers="headers" :items="items" />
    </div>
</template>
