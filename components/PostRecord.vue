<script setup lang='ts'>
import type { Category } from '@/interfaces'
let selector: string
const categoryList = ref<Category[]>()
const asyncData = await useFetch(
  '/api/getCategories',
  {
    key: `/api/getCategories`,
  },
)

const data = asyncData.data.value as Category[]

// category 加工
if (data != undefined) { // 取得済の場合のみ
  for (const d of data) {
    // 100, category_name -> 100:category_name という表示に
    // ただし加工済の場合は skip
    if (d.category_name[3] != ':') {
      d.category_name = d.category_id + ':' + d.category_name
    }
  }
}

categoryList.value = data

// pricebox
const priceBox = ref<number>()

const postButton = async (): Promise<void> => {
  await useAsyncData(
    `record`,
    (): Promise<unknown> => {
      const send_category_id = selector.slice(0, 3) // 210-食費→210
      const param = { price: priceBox.value, category_id: send_category_id }
      const paramStr = '?price=' + param['price'] + '&category_id=' + param['category_id']
      const localurl = '/api/postRecord' + paramStr
      const response = $fetch(localurl)
      return response
    },
  )
  location.reload()
}

</script>

<template>
  <div class='container text-center'>
    <div class='row justify-content-center'>
      <div class='col-2'>
        <select v-model='selector' class='form-select'>
          <option v-for='category in categoryList' :key='category.category_id'>
            {{ category.category_name }}
          </option>
        </select>
      </div>

      <div class='col-2 mb-3'>
        <input v-model='priceBox' type='number' placeholder='Value' />
      </div>
    </div>

    <div class='d-grid col-2 mx-auto'>
      <button class='btn btn-primary' @click='postButton' name='postButton' type='submit'>Post</button>
    </div>

  </div>
</template>
