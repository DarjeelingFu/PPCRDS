<script setup>
import { use } from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, onMounted, provide, ref } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import { useStore } from '../stores'

use([TitleComponent, LegendComponent, RadarChart, CanvasRenderer])
provide(THEME_KEY, 'dark');

const store = useStore()

let option = computed(() => ({
  radar: {
    // shape: 'circle',
    center: ['50%', '57%'],
    indicator: [
      { name: '高兴', max: Math.min(Math.max(...store.emotion), 1) },
      { name: '平静', max: Math.min(Math.max(...store.emotion), 1) },
      { name: '悲伤', max: Math.min(Math.max(...store.emotion), 1) },
      { name: '厌恶', max: Math.min(Math.max(...store.emotion), 1) },
      { name: '恐惧', max: Math.min(Math.max(...store.emotion), 1) },
    ],
    splitLine: {
      lineStyle: {
        opacity: 0.6
      }
    },
    axisLine: {
      lineStyle: {
        opacity: 0.6
      }
    }
  },
  series: [
    {
      name: 'emotion',
      type: 'radar',
      data: [
        {
          value: store.emotion,
          name: 'emotions'
        }
      ],
      lineStyle: {
        width: 2,
        opacity: 1
      },
      areaStyle: {
        opacity: 0.5
      },
      animation: true,
    }
  ]
}))

const chart = ref(null)

const handleResize = () => {
  chart.value.resize()
  chart.value.clear()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})
</script>

<template>
  <div id="container">
    <div id="panel">
      <span id="title">情绪雷达图</span>
      <div id="charts">
        <v-chart id="chartEmotion" :option="option" ref="chart"/>
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
  /* background: radial-gradient(circle, #100b2b, #191b68); */
  background: #100b2b;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
}

#title {
  color: rgb(255, 255, 255);
  width: 100%;
  font-size: 16px;
  /* text-align: center; */
  height: 30px;
}

#charts {
  display: flex;
  justify-content: space-around;
  height: calc(100% - 30px);
}

#chartEmotion {
  height: calc(100%);
  width: 100%;
}
</style>