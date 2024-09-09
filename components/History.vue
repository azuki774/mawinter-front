<script setup lang='ts'>
import type { Record } from '@/interfaces'
const config = useRuntimeConfig() // nuxt.config.ts に書いてあるコンフィグを読み出す
const recordList = ref<Record[]>()
const asyncData = await useFetch(
  '/api/history',
  {
    key: `/api/history`,
  }
)


const data = asyncData.data.value as Record[]

// fetchデータを整形
if (data != undefined) { // 取得済の場合のみ
  for (let d of data) {
    d.datetime = d.datetime.slice(0, 19) // 2023-09-23T00:00:00+09:00 -> 2023-09-23T00:00:00
  }
}


recordList.value = data

async function showDeleteDialog(id: number): Promise<void> {
  const userResponse: boolean = confirm('このデータを削除しますか')
  if (userResponse == true) {
    console.log('delete: id=' + id)
    const asyncDataBtn = await useAsyncData(
      `record`,
      (): Promise<any> => {
        const param = { 'id': id }
        const paramStr = '?id=' + param['id']
        const localurl = '/api/deleteRecord' + paramStr
        const response = $fetch(localurl)
        return response
      }
    )
    location.reload()
  }

}

</script>

<template>
  <div class='container-sm'>
    <table class='table table-striped table-sm'>
      <thead>
        <tr>
          <th>ID</th>
          <th>カテゴリ名</th>
          <th>金額</th>
          <th>日付</th>
          <th>メモ</th>
          <th>削除</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for='record in recordList'>
          <td>{{ record.id }}</td>
          <td>{{ record.category_name }}</td>
          <td>{{ record.price }}</td>
          <td>{{ record.datetime }}</td>
          <td>{{ record.memo }}</td>
          <td><button class='btn btn-secondary' @click='showDeleteDialog(record.id)'>削除</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
