<script setup>
import { onMounted, ref, watch } from 'vue'
import { useStore } from '../stores'

const store = useStore()

</script>

<template>
  <div id="container">
    <div id="panel">
      <span id="areaTitle">脑电地形图</span>
      <div class="rowFlex">
        <div id="topographyA" class="topography">A</div>
        <div id="topographyB" class="topography">B</div>
      </div>
      <div class="rowFlex">
        <div id="topographyC" class="topography">C</div>
        <div id="topographyD" class="topography">D</div>
      </div>
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
}

#areaTitle {
  display: block;
  color: white;
  font-size: 16px;
  height: 30px;
}

.rowFlex {
  display: flex;
  justify-content: space-between;
  height: calc((100% - 30px) * 0.5);
  width: 100%;
}

.topography {
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;

  color: white;
  font-size: 24px;
  font-weight: bold;
}

</style>