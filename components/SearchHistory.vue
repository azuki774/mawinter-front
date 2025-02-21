<script setup lang='ts'>
import { ref } from 'vue'
import type { Record } from '@/interfaces'
import type { Header, Item } from 'vue3-easy-data-table'

const asyncData = await useFetch(
  '/api/getHistories?yyyymm=202502&category_id=200', // TODO
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

const headers = ref<Header[]>([
  { text: 'ID', value: 'id' },
  { text: 'カテゴリ名', value: 'category_name', sortable: true },
  { text: '利用日', value: 'datetime', sortable: true },
  { text: '登録元', value: 'from' },
  { text: '金額', value: 'price', sortable: true },
  { text: 'メモ', value: 'memo' },
])

const items = ref<Item[]>(data)

const options_yyyymm = ref([
  { value: '202502', label: '202502' },
  { value: '202501', label: '202501' },
  { value: '202412', label: '202412' },
])

const selected_yyyymm_Value = ref('')

// 選択変更時に実行する処理
watch(selected_yyyymm_Value, (newValue) => {
  const fetchData = useFetch(
    '/api/getHistories?yyyymm=' + newValue + '&category_id=200', // TODO
    {
      key: `/api/getHistories`,
    },
  )
  items.value = fetchData.data.value as Record[]
})

</script>

<template>
      <div class='row justify-content-center'>
      <h2>レコード</h2>
      <div>
        <label for="dropdown">取得月:</label>
        <select id="dropdown" v-model="selected_yyyymm_Value">
          <option value="" disabled>選択してください</option>
          <option v-for="option in options_yyyymm" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
        <p>選択された値: {{ selected_yyyymm_Value }}</p>
      </div>
      <EasyDataTable :headers="headers" :items="items" />
    </div>
</template>
