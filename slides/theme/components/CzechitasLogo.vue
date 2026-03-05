<script setup>
import logo from '../assets/czechitas-logo.png'

defineProps({
  size: {
    type: String,
    default: 'small',
    validator: (v) => ['small', 'medium', 'large'].includes(v),
  },
  invert: {
    type: Boolean,
    default: false,
  },
})

const sizeMap = {
  small: '120px',
  medium: '180px',
  large: '260px',
}
</script>

<template>
  <img
    :src="logo"
    alt="Czechitas"
    :style="{ width: sizeMap[size], height: 'auto' }"
    :class="{ inverted: invert }"
  />
</template>

<style scoped>
.inverted {
  filter: brightness(0) invert(1);
  opacity: 0.9;
}
</style>
