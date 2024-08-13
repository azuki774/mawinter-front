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
categoryList.value = data

// pricebox
const priceBox = ref<number>()

const postButton = async (): Promise<void> => {
  console.log('start')
  const asyncData = await useAsyncData(
    `record`,
    (): Promise<any> => {
      const url = "/api/postRecord"
      const response = $fetch(url);
      console.log('response')
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
