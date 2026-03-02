<script setup>
import { computed } from 'vue'

const props = defineProps({
  url: { type: String, required: true },
  size: { type: Number, default: 160 },
  dark: { type: String, default: '#2D2E83' },
  light: { type: String, default: '#ffffff' },
})

const imgSrc = computed(() => {
  const encoded = encodeURIComponent(props.url)
  const px = props.size * 2
  const dk = props.dark.replace('#', '')
  const lt = props.light.replace('#', '')
  return `https://api.qrserver.com/v1/create-qr-code/?size=${px}x${px}&data=${encoded}&color=${dk}&bgcolor=${lt}`
})
</script>

<template>
  <div class="qr-wrapper" :style="{ width: size + 'px' }">
    <img :src="imgSrc" :alt="url" :width="size" :height="size" />
    <span v-if="$slots.default" class="qr-label"><slot /></span>
  </div>
</template>

<style scoped>
.qr-wrapper {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3em;
}

.qr-wrapper img {
  border-radius: 6px;
}

.qr-label {
  font-size: 0.7em;
  font-weight: 400;
  color: #666;
  text-align: center;
}
</style>
