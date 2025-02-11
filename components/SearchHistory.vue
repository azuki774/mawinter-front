<script setup lang='ts'>
import { ref } from 'vue'
import type { Header, Item } from 'vue3-easy-data-table'

const headers = ref<Header[]>([
  { text: 'ID', value: 'id' },
  { text: 'カテゴリ名', value: 'category_name', sortable: true },
  { text: '利用日', value: 'datetime' },
  { text: '登録元', value: 'from' },
  { text: '金額', value: 'price', sortable: true },
  { text: 'メモ', value: 'memo' },
])

const items = ref<Item[]>([
  { id: '1', category_name: 'カテゴリ名', datetime: '2025-01-01', from: 'テスト', price: 1234, memo: 'メモ欄' },
])

const addItem = () => {
  items.value = [
    { id: '2', category_name: '新しいカテゴリ', datetime: '2025-02-01', from: 'テスト2', price: 5678, memo: '新しいメモ' },
    { id: '3', category_name: '別のカテゴリ', datetime: '2025-03-01', from: 'テスト3', price: 91011, memo: '別のメモ' },
  ]
}

</script>

<template>
    <div class='container text-center'>
      <div class='row justify-content-center'>
        <EasyDataTable :headers="headers" :items="items" />
        <button @click="addItem">アイテムを追加</button>
      </div>
    </div>
</template>
