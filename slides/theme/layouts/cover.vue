<script setup>
import characterImg from '../assets/czechitas-woman-laptop.png'

defineProps({
  subtitle: { type: String, default: '' },
  author: { type: String, default: '' },
  date: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout cover czechitas-gradient-bg">
    <div class="cover-content">
      <div class="cover-text">
        <div class="title">
          <slot />
        </div>
        <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
        <div class="meta">
          <p v-if="author" class="author">{{ author }}</p>
          <p v-if="date" class="date">{{ date }}</p>
        </div>
      </div>
      <div class="cover-character">
        <img :src="characterImg" alt="" />
      </div>
    </div>
    <div class="cover-logo">
      <CzechitasLogo size="medium" :invert="true" />
    </div>
  </div>
</template>

<style scoped>
.cover {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 3rem 4rem;
  position: relative;
  overflow: hidden;
  height: 100%;
}

.cover-content {
  flex: 1;
  display: flex;
  align-items: center;
  z-index: 1;
}

.cover-text {
  max-width: 55%;
}

.title :deep(h1) {
  color: #ffffff;
  font-size: 2.75rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.35rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 0.75rem;
}

.meta {
  margin-top: 1.5rem;
}

.author,
.date {
  font-size: 1rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.85);
  margin: 0.15rem 0;
}

.cover-character {
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-55%);
}

.cover-character img {
  height: 420px;
  width: auto;
  object-fit: contain;
}

.cover-logo {
  position: absolute;
  bottom: 1.5rem;
  right: 2.5rem;
  z-index: 2;
}
</style>
