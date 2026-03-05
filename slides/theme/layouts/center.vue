<template>
  <div class="slidev-layout center-layout">
    <div class="center-content">
      <slot />
    </div>
    <div class="footer-logo">
      <CzechitasLogo size="small" />
    </div>
  </div>
</template>

<style scoped>
.center-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2.5rem 3rem;
  position: relative;
  height: 100%;
  background: #ffffff;
  text-align: center;
}

.center-content {
  max-width: 80%;
}

.center-content :deep(h1) {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.footer-logo {
  position: absolute;
  bottom: 1.25rem;
  right: 1.75rem;
  opacity: 0.85;
}
</style>
