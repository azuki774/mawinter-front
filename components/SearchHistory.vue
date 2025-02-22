<script setup lang='ts'>
import { ref } from 'vue'
import type { Category, Record } from '@/interfaces'
import type { Header, Item } from 'vue3-easy-data-table'
const allCategoryText: string = '全カテゴリ'

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

const options_categoryID = ref<Category[]>([])

const asyncHistoryData = await $fetch(`/api/getHistories`)
const historyData = asyncHistoryData as Record[]

// fetchデータを整形
if (historyData != undefined) { // 取得済の場合のみ
  for (const d of historyData) {
    d.datetime = d.datetime.slice(0, 19) // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
  }
}

const items = ref<Item[]>(historyData)

const selected_yyyymm_value = ref(options_yyyymm.value[0].value) // 第1項目をデフォに, TODO
const selected_categoryID_value = ref<string | null>(null) // 実際に選択されている値が入る

onMounted(async () => {
  const asyncHistoryData = await $fetch(`/api/getHistories`)
  const historyData = asyncHistoryData as Record[]
  // fetchデータを整形
  if (historyData != undefined) { // 取得済の場合のみ
    for (const d of historyData) {
      d.datetime = d.datetime.slice(0, 19) // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
    }
  }

  const asyncCategoryData = await $fetch(`/api/getCategories`)
  options_categoryID.value = asyncCategoryData as Category[]
  const allCategory: Category = {
    category_id: 0,
    category_name: allCategoryText,
  }
  options_categoryID.value.unshift(allCategory) // 全カテゴリをカテゴリの先頭に追加
  if (options_categoryID.value.length > 0) {
    await nextTick()
    selected_categoryID_value.value = String(options_categoryID.value[0].category_id)
  }
})

const fetchData = async (yyyymm: string, categoryID: string) => {
  try {
    let query = `?yyyymm=${yyyymm}`
    // categoryID が null または undefined の場合、'-1' に置き換える
    const validCategoryID = categoryID ? categoryID : '-1'

    if (validCategoryID !== '-1') {
      // パラメータが不正なときは何もしない
      return
    }

    if (validCategoryID != '0') {
      // 0 = 全カテゴリ
      query += `&category_id=${validCategoryID}`
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
    fetchData(new_yyyymm_value, String(new_categoryID_value))
  },
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
        <label for="dropdown">カテゴリ名:</label>
        <select id="dropdown" v-model="selected_categoryID_value">
          <option v-for="option in options_categoryID" :key="option.category_id" :value="option.category_id">
            {{ option.category_name }}
          </option>
        </select>
      </div>

      <EasyDataTable :headers="headers" :items="items" />
    </div>
</template>
