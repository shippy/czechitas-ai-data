<script setup>
import { computed } from 'vue'

const props = defineProps({
  image: { type: String, required: true },
})

const base = import.meta.env.BASE_URL || '/'
const imageSrc = computed(() => {
  if (props.image.startsWith('/') && !props.image.startsWith('//')) {
    return base.replace(/\/$/, '') + props.image
  }
  return props.image
})
</script>

<template>
  <div class="slidev-layout image-right">
    <div class="left-content">
      <slot />
    </div>
    <div class="right-image">
      <img :src="imageSrc" alt="" />
    </div>
    <div class="footer-logo">
      <CzechitasLogo size="small" />
    </div>
  </div>
</template>

<style scoped>
.image-right {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2rem;
  padding: 2.5rem 0 2rem 3rem;
  position: relative;
  height: 100%;
  background: #ffffff;
  align-items: center;
}

.left-content {
  padding-right: 1rem;
}

.left-content :deep(h1) {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.right-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.right-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.footer-logo {
  position: absolute;
  bottom: 1.25rem;
  right: 1.75rem;
  opacity: 0.85;
}
</style>
