<script setup lang='ts'>
import { ref } from 'vue'
import type { Record } from '@/interfaces'
import type { Header, Item } from 'vue3-easy-data-table'

const headers = ref<Header[]>([
  { text: 'ID', value: 'id' },
  { text: 'カテゴリ名', value: 'category_name', sortable: true },
  { text: '利用日', value: 'datetime', sortable: true },
  { text: '登録元', value: 'from' },
  { text: '金額', value: 'price', sortable: true },
  { text: 'メモ', value: 'memo' },
])

const options_yyyymm = ref([
  { value: '202502', label: '202502' },
  { value: '202501', label: '202501' },
  { value: '202412', label: '202412' },
])

const options_categoryID = ref([
  { value: 'all', label: 'all' },
  { value: '200', label: '200' },
  { value: '210', label: '210' },
  { value: '220', label: '220' },
])

const asyncData = await useFetch(
  '/api/getHistories',
  {
    key: `/api/getHistories`,
  },
)

const data = asyncData.data.value as Record[]

// fetchデータを整形
if (data != undefined) { // 取得済の場合のみ
  for (const d of data) {
    d.datetime = d.datetime.slice(0, 19) // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
  }
}

const selected_yyyymm_value = ref(options_yyyymm.value[0].value) // 第1項目をデフォに
const selected_categoryID_value = ref(options_categoryID.value[0].value) // 第1項目をデフォに

const items = ref<Item[]>(data)

const fetchData = async (yyyymm: string, categoryID: string) => {
  try {
    let query = `?yyyymm=${yyyymm}`
    if (categoryID !== 'all') {
      query += `&category_id=${categoryID}`
    }

    const data = await $fetch(`/api/getHistories${query}`)
    items.value = data as Record[]
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  catch (error) {
    // ToDo: error handling
    // console.error('Error fetching data:', error)
  }
}

// 選択変更時に実行する処理
watch(
  [selected_yyyymm_value, selected_categoryID_value],
  ([new_yyyymm_value, new_categoryID_value]) => {
    fetchData(new_yyyymm_value, new_categoryID_value)
  },
  { immediate: true },
)
</script>

<template>
    <div class='row justify-content-center'>
      <h2>レコード</h2>

      <div class='col-2 mb-3'>
        <label for="dropdown">取得月:</label>
        <select id="dropdown" v-model="selected_yyyymm_value">
          <option v-for="option in options_yyyymm" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class='col-2 mb-3'>
        <label for="dropdown">カテゴリID:</label>
        <select id="dropdown" v-model="selected_categoryID_value">
          <option v-for="option in options_categoryID" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <EasyDataTable :headers="headers" :items="items" />
    </div>
</template>
