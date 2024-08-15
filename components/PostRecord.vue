<script setup lang="ts">
import type { Category } from "@/interfaces";
const config = useRuntimeConfig(); // nuxt.config.ts に書いてあるコンフィグを読み出す
const selector = ref<any>()
const categoryList = ref<Category[]>()
const asyncData = await useFetch(
  "/api/getCategories",
  {
    key: `/api/getCategories`,
  }
);

const data = asyncData.data.value as Category[];

// category 加工
if (data != undefined) { // 取得済の場合のみ
  for (let d of data) {
    // 100, category_name -> 100:category_name という表示に
    // ただし加工済の場合は skip
    if (d.category_name[3] != ":") {
      d.category_name = d.category_id + ":" + d.category_name
    }
  }
}

categoryList.value = data

// pricebox
const priceBox = ref<number>()

const postButton = async (): Promise<void> => {
  const asyncDataBtn = await useAsyncData(
    `record`,
    (): Promise<any> => {
      const send_category_id = selector.value.slice(0, 3) // 210-食費→210
      const param = { 'price': priceBox.value, 'category_id': send_category_id }
      const paramStr = "?price=" + param['price'] + "&category_id=" + param['category_id']
      const localurl = "/api/postRecord" + paramStr
      const response = $fetch(localurl);
      return response;
    }
  );
  location.reload()
};

</script>

<template>
  <container>
    <Row justify-content="md-center">
      <Col col="md-auto">
      <BFormSelect v-model="selector" margin="b-4">
        <b-option v-for="category in categoryList" :key="category.category_id">
          {{ category.category_name }}
        </b-option>
      </BFormSelect>
      </Col>

      <Col col="md-auto">
      <BFormFloating margin="b-2">
        <BFormInput v-model="priceBox" type="number" placeholder="name@example.com" />
        <BFormLabel for="floatingInput">
          Price
        </BFormLabel>
      </BFormFloating>
      </Col>
    </Row>

    <Col display="grid" gap="2" margin="x-auto" col="6">
    <b-button button="primary" size="lg" @click="postButton" name="postButton" class="sendbutton"
      type="submit">Post</b-button>
    </Col>
  </container>
</template>
