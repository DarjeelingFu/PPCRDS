<script setup>
import { useStore } from '../stores'

const store = useStore()
</script>

<template>
  <div id="container">
    <div id="panel">
      <!-- <video id="camera" :src="url" autoplay></video> -->
      <img :src="store.videoSrc" id="camera">
    </div>
  </div>
</template>

<style scoped>
#container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#panel {
  width: calc(100% - 20px);
  height: calc(100% - 20px);
  background: #100b2b;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#camera {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>