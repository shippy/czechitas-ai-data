<script setup>
import { computed } from 'vue'

const props = defineProps({
  image: { type: String, default: '' },
  name: { type: String, default: '' },
  subtitle: { type: String, default: '' },
})

const base = import.meta.env.BASE_URL || '/'
const imageSrc = computed(() => {
  if (props.image && props.image.startsWith('/') && !props.image.startsWith('//')) {
    return base.replace(/\/$/, '') + props.image
  }
  return props.image
})
</script>

<template>
  <div class="slidev-layout bio">
    <div class="bio-left">
      <div class="bio-photo">
        <img v-if="image" :src="imageSrc" :alt="name" class="photo" />
        <div v-else class="photo-placeholder"></div>
      </div>
      <div class="bio-qr">
        <slot name="qr" />
      </div>
    </div>
    <div class="bio-text">
      <h1 v-if="name" class="name">{{ name }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
      <div class="bio-body">
        <slot />
      </div>
    </div>
    <div class="footer-logo">
      <CzechitasLogo size="small" />
    </div>
  </div>
</template>

<style scoped>
.bio {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  padding: 3rem 3.5rem;
  position: relative;
  height: 100%;
  background: #ffffff;
  align-items: center;
}

.bio-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
}

.bio-photo {
  display: flex;
  justify-content: center;
  align-items: center;
}

.photo {
  width: 250px;
  height: 250px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center 20%;
}

.photo-placeholder {
  width: 250px;
  height: 250px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E6007E 0%, #6B1FA0 50%, #00BFE7 100%);
  opacity: 0.3;
}

.bio-qr {
  display: flex;
  justify-content: center;
}

.name {
  font-size: 2rem;
  font-weight: 800;
  color: var(--czechitas-blue, #2D2E83);
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--czechitas-pink, #E6007E);
  margin-bottom: 1rem;
}

.bio-body {
  font-weight: 300;
}

.footer-logo {
  position: absolute;
  bottom: 1.25rem;
  right: 1.75rem;
  opacity: 0.85;
}
</style>
