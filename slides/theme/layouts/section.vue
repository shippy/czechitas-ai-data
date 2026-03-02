<script setup>
defineProps({
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout section czechitas-gradient-bg">
    <div class="section-content">
      <div class="title">
        <slot />
      </div>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
  </div>
</template>

<style scoped>
.section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem 4rem;
  text-align: center;
  height: 100%;
}

.section-content {
  max-width: 80%;
}

.title :deep(h1) {
  color: #ffffff;
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.15;
}

.subtitle {
  font-size: 1.25rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 1rem;
}
</style>
