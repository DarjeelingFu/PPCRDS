<script setup>
import { onMounted, ref, watch } from 'vue'
import { useStore } from '../stores'

const store = useStore()

</script>

<template>
  <div id="container">
    <div id="panel">
      
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
  width: calc(100% - 40px);
  height: calc(100% - 40px);
  background: #100b2b;
  border-radius: 5px;
  margin: 5px;
  padding: 15px;
}

</style>