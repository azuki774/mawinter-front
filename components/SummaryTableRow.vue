<template>
  <tr :class="className">
    <td class="text-center">{{ item.category_id }}</td>
    <td>{{ item.category_name }}</td>
    <td v-for="(price, index) in item.price" :key="index" class="text-end">
      {{ price.toLocaleString() }}
    </td>
    <td class="text-end">
      {{ item.total.toLocaleString() }}
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { SummaryOne } from '@/interfaces'

interface Props {
  item: SummaryOne
  className?: string
}

defineProps<Props>()
</script>
