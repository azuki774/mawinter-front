<script setup lang="ts">
import type { Category } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const categoryList = ref<Category[]>()
const asyncData2 = await useAsyncData(
  `records`,
  (): Promise<any> => {
    const url = config.public.mawinterApi + "/categories";
    const response = $fetch(url);
    return response;
  }
  );

const data2 = asyncData2.data.value as Category[];
categoryList.value = data2

</script>

<template>
  <section>
    <select name="categorySelector">
      <option v-for="category in categoryList" :key="categoryList">
        {{ category.category_name }}
      </option>
    </select>
  </section>
</template>
