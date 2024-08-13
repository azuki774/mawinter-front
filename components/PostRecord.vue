<script setup lang="ts">
import type { Category } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const categoryList = ref<Category[]>()
const asyncData = await useAsyncData(
  `records`,
  (): Promise<any> => {
    const url = config.public.mawinterApi + "/categories";
    const response = $fetch(url);
    return response;
  }
);

const data = asyncData.data.value as Category[];
// category 加工
for (let d of data) {
  // 100, category_name -> 100:category_name という表示に
  // ただし加工済の場合は skip
  if (d.category_name[3] != ":") {
    d.category_name = d.category_id + ":" + d.category_name
  }
}


categoryList.value = data

// pricebox
const priceBox = ref<number>()

const postButton = async (): Promise<void> => {
  const asyncData = await useAsyncData(
    `record`,
    (): Promise<any> => {
      const param = { 'price': priceBox.value, 'category_id': 200 } // TODO: 固定値
      const paramStr = "?price=" + param['price'] + "&category_id=" + param['category_id']
      const localurl = "/api/postRecord" + paramStr
      const response = $fetch(localurl);
      return response;
    }
  );
};

</script>

<template>
  <section>

    <select name="categorySelector">
      <option v-for="category in categoryList" :key="category.category_id">
        {{ category.category_name }}
      </option>
    </select>

    <input v-model="priceBox" type="number" />

    <div class="col">
      <button @click="postButton" name="postButton" class="sendbutton" type="submit">Post</button>
    </div>

  </section>
</template>
