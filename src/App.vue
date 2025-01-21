<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { onMounted, onBeforeUnmount } from 'vue'

const router = useRouter()

function toggleAbout() {
  if (router.currentRoute.value.name === 'about') {
    router.replace('/')
  } else {
    router.replace('/about')
  }
}

function handleKeyPress(event: KeyboardEvent) {
  if (event.key === 'F1') {
    
    toggleAbout()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
})

</script>

<template>
  <RouterView />
</template>
