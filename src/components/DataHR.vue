<script setup>
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from 'echarts/components'
import { ScatterChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, provide } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import { useStore } from '../stores'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LineChart,
  CanvasRenderer,
  ScatterChart
])
provide(THEME_KEY, 'dark');

const store = useStore()

const optionHRS = computed(() => ({
  tooltip: {},
  xAxis: {
    type: 'value',
    splitLine: { show: false }, // Hide grid lines
    // min: 20,
    // max: 200
  },
  yAxis: {
    type: 'value',
    splitLine: { show: false }, // Hide grid lines
    axisLabel: { show: false },
    axisTick: { show: false },
    position: 'left',
    // max: (Math.floor(10000 * (1 / (store.variance * Math.sqrt(2 * Math.PI)))) + 1) / 10000
  },
  series: [{
    type: 'line',
    data: Array.from({ length: 200 }, (_, i) => {
      const x = (i);
      const y = (1 / (store.variance * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * Math.pow((x - store.mean) / store.variance, 2));
      return [x, y];
    }),
    showSymbol: false,
  },
  {
    type: 'line',
    data: [[store.value, 0], [store.value, (1 / (store.variance * Math.sqrt(2 * Math.PI)))]], // Adjust the y values as needed
    lineStyle: {
      color: 'yellow',
      type: 'solid'
    },
    showSymbol: false,
  }],
  grid: {
    left: '10%',
    right: '10%',
    top: '10%',
    bottom: '10%',
  }
}))
const optionSTG = computed(() => ({
  xAxis: { splitLine: { show: false } },
  yAxis: { splitLine: { show: false } },
  series: [
    {
      symbolSize: 20,
      data: store.corrdinates.slice(0, 59),
      type: 'scatter'
    },
    {
      symbolSize: 20,
      data: [store.corrdinates[59]],
      type: 'scatter',
      itemStyle: {
        color: 'yellow'
      }
    }
  ],
  grid: {
    left: '10%',
    right: '10%',
    top: '10%',
    bottom: '10%',
  }
}))

</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="charts">
        <div id="chartLeft">
          <span>心理稳定性</span>
          <v-chart id="chartHRS" :option="optionHRS" autoresize />
        </div>
        <div id="chartRight">
          <span>离群值</span>
          <v-chart id="chartSTG" :option="optionSTG" autoresize />
        </div>
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
}

#charts {
  display: flex;
  justify-content: space-around;
  height: calc(100% - 30px);
}

#charts span {
  display: block;
  color: white;
  font-size: 16px;
  height: 30px;
}

#chartLeft,
#chartRight {
  height: calc(100% - 30px);
  width: 50%;
}

#chartHRS {
  width: 100%;
  height: 100%;
}
</style>