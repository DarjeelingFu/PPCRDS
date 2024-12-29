<script setup>
import { use } from 'echarts/core'
import { ScatterChart, BarChart } from 'echarts/charts'
import { GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import VChart, { THEME_KEY } from 'vue-echarts';
import { provide } from 'vue';
import { useStore } from '../stores'
import { computed } from 'vue';
import { graphic } from 'echarts';

provide(THEME_KEY, 'dark');
use([GridComponent, ScatterChart, BarChart, CanvasRenderer])

const store = useStore()

const optionHR = computed(() => ({
  yAxis: {
    show: false,
    boundaryGap: false,
    data: [
      'A'
    ]
  },
  xAxis: {
    interval: 60,
    type: 'value',
    boundaryGap: true,
    max: 180,
    splitLine: {
      show: false
    },
    axisLabel: {
      formatter: '{value}',
      color: '#ffffff',
      margin: -12,
    }
  },
  series: [
    {
      type: 'scatter',
      symbol: 'path://M50 85 L90 15 L10 15 Z',
      silent: false,
      itemStyle: {
        normal: {
          color: 'rgba(255,0,0,1.0)',
          borderColor: '#000',
          borderWidth: 1
        }
      },
      symbolSize: [10, 20],
      symbolOffset: ['0%', '0%'],
      z: 20,
      data: [store.heartRate],
      label: {
        normal: {
          show: true,
          formatter: function (param) {
            return param.data + ' bpm';
          },
          position: 'top',
          color: '#ffffff', // Change label color to white
          fontSize: 14 // Increase font size
        }
      },
    },
    {
      type: 'bar',
      silent: true,
      animation: false,
      barWidth: 8,
      itemStyle: {
        normal: {
          color: new graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#00c0ff' },
            { offset: 0.5, color: '#5af98d' },
            { offset: 1, color: '#f07d2e' }
          ])
        }
      },
      stack: 'total',
      data: [180]
    },
  ]
}));

const optionBR = computed(() => ({
  yAxis: {
    show: false,
    boundaryGap: false,
    data: [
      'A'
    ]
  },
  xAxis: {
    interval: 12,
    type: 'value',
    boundaryGap: true,
    max: 36,
    splitLine: {
      show: false
    },
    axisLabel: {
      formatter: '{value}',
      color: '#ffffff',
      margin: -12,

    }
  },
  series: [
    {
      type: 'scatter',
      symbol: 'path://M50 85 L90 15 L10 15 Z',
      silent: false,
      itemStyle: {
        normal: {
          color: 'rgba(255,0,0,1.0)',
          borderColor: '#000',
          borderWidth: 1
        }
      },
      symbolSize: [10, 20],
      symbolOffset: ['0%', '0%'],
      z: 20,
      data: [store.respiration],
      label: {
        normal: {
          show: true,
          formatter: function (param) {
            return param.data + ' 次/分';
          },
          position: 'top',
          color: '#ffffff', // Change label color to white
          fontSize: 14 // Increase font size

        }
      },
    },
    {
      type: 'bar',
      silent: true,
      animation: false,
      barWidth: 8,
      itemStyle: {
        normal: {
          color: new graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#00c0ff' },
            { offset: 0.5, color: '#5af98d' },
            { offset: 1, color: '#f07d2e' }
          ])
        }
      },
      stack: 'total',
      data: [36]
    },]
}))

const optionEN = computed(() => ({
  yAxis: {
    show: false,
    boundaryGap: false,
    data: [
      'A'
    ]
  },
  xAxis: {
    interval: 0.5,
    type: 'value',
    boundaryGap: true,
    max: 1,
    splitLine: {
      show: false
    },
    axisLabel: {
      formatter: (value) => {
        return (value * 100).toFixed(0) + '%';
      },
      color: '#ffffff',
      margin: -12,
    }
  },
  series: [
    {
      type: 'scatter',
      symbol: 'path://M50 85 L90 15 L10 15 Z',
      silent: false,
      itemStyle: {
        normal: {
          color: 'rgba(255,0,0,1.0)',
          borderColor: '#000',
          borderWidth: 1,
        }
      },
      symbolSize: [10, 20],
      symbolOffset: ['0%', '0%'],
      z: 20,
      data: [store.leftEnergy],
      label: {
        normal: {
          show: true,
          formatter: function (param) {
            return (param.value * 100).toFixed(0) + '%';
          },
          position: 'top',
          color: '#ffffff', // Change label color to white
          fontSize: 14 // Increase font size
        }
      },
    },
    {
      type: 'bar',
      silent: true,
      animation: false,
      barWidth: 8,
      itemStyle: {
        normal: {
          color: new graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#00c0ff' },
            { offset: 0.5, color: '#5af98d' },
            { offset: 1, color: '#f07d2e' }
          ])
        }
      },
      stack: 'total',
      data: [36]
    },
  ]
}))

</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="title">基本生命特征</div>
      <div id="charts">
        <div id="HR">
          <span>心率</span>
          <v-chart id="chartHR" :option="optionHR" autoresize />
          <!-- <span>正常</span> -->
        </div>
        <div id="HR">
          <span>呼吸</span>
          <v-chart id="chartHR" :option="optionBR" autoresize />
          <!-- <span>正常</span> -->
        </div>
        <div id="HR">
          <span>剩余<br />体能</span>
          <v-chart id="chartHR" :option="optionEN" autoresize />
          <!-- <span>正常</span> -->
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
  color: white;
  width: 100%;
  font-size: 16px;
  /* text-align: center; */
}

#charts {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: calc(100% - 30px);
}

#HR {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

#HR span {
  color: white;
  white-space: nowrap;
}
</style>