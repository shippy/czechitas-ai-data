<template>
  <div class="slidev-layout default">
    <div class="content">
      <slot />
    </div>
    <div class="footer-logo">
      <CzechitasLogo size="small" />
    </div>
  </div>
</template>

<style scoped>
.default {
  padding: 2.5rem 3rem 2rem;
  position: relative;
  height: 100%;
  background: #ffffff;
}

.content {
  height: 100%;
}

.content :deep(h1) {
  font-size: 2rem;
  margin-bottom: 1.25rem;
}

.footer-logo {
  position: absolute;
  bottom: 1.25rem;
  right: 1.75rem;
  opacity: 0.85;
}
</style>
