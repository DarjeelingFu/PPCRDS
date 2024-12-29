<script setup>
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, provide } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import { graphic } from 'echarts';
import { useStore } from '../stores';

use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  GridComponent,
  LineChart,
  CanvasRenderer
])

provide(THEME_KEY, 'dark');

const store = useStore()

const option = computed(() => ({
  color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00'],
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['平静', '悲伤', '厌恶', '愤怒', '高兴'],
    textStyle: {
      fontSize: 15
    },
    top: '0%'
  },
  grid: {
    left: '5%',
    right: '5%',
    bottom: '8%',
    top: '12%',
    containLabel: false
  },
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      data: Array.from({ length: 30 }, (_, i) => i - 29)
    }
  ],
  yAxis: [
    {
      type: 'value',
      min: 0,
      max: 1,
      show: false
    },
    {
      type: 'value',
      show: false
    }
  ],
  series: [
    {
      name: '平静',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(128, 255, 165)'
          },
          {
            offset: 1,
            color: 'rgb(1, 191, 236)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: store.emotionHistory[0]
    },
    {
      name: '悲伤',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(0, 221, 255)'
          },
          {
            offset: 1,
            color: 'rgb(77, 119, 255)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: store.emotionHistory[1]
    },
    {
      name: '厌恶',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(55, 162, 255)'
          },
          {
            offset: 1,
            color: 'rgb(116, 21, 219)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: store.emotionHistory[2]
    },
    {
      name: '愤怒',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 0, 135)'
          },
          {
            offset: 1,
            color: 'rgb(135, 0, 157)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: store.emotionHistory[3]
    },
    {
      name: '高兴',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      label: {
        show: true,
        position: 'top'
      },
      areaStyle: {
        opacity: 0.8,
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 191, 0)'
          },
          {
            offset: 1,
            color: 'rgb(224, 62, 76)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: store.emotionHistory[4]
    }
  ]
}))
</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="charts">
        <div id="chartEmotionHistory">
          <span>实时情绪变化</span>
          <v-chart id="chartHRS" :option="option" autoresize />
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
  height: 30px;
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

#chartEmotionHistory {
  height: calc(100% - 30px);
  width: 100%;
}
</style>