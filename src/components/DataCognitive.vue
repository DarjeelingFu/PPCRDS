<script setup>
import { use } from 'echarts/core'
import { GaugeChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, provide } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import { useStore } from '../stores';

use([GaugeChart, CanvasRenderer])
provide(THEME_KEY, 'dark');

const store = useStore()

const optionCL = computed(() => ({
  series: [
    {
      type: 'gauge',
      center: ['50%', '60%'],
      radius: '85%',
      min: 0,
      max: 1,
      splitNumber: 8,
      axisLine: {
        lineStyle: {
          width: 10,
          color: [
            [0.25, '#7CFFB2'],
            [0.5, '#58D9F9'],
            [0.75, '#FDDD60'],
            [1, '#FF6E76']
          ]
        }
      },
      axisLabel: {
        color: '#fff',
        fontSize: 16,
        distance: -45,
        formatter: function (value) {
          if (value === 0.875) {
            return '高';
          } else if (value === 0.625) {
            return '中';
          } else if (value === 0.375) {
            return '低';
          } else if (value === 0.125) {
            return '无';
          }
          return '';
        }
      },
      pointer: {
        itemStyle: {
          color: function (value) {
            if (value > 0.75) {
              return '#7CFFB2';
            } else if (value > 0.5) {
              return '#58D9F9';
            } else if (value > 0.25) {
              return '#FDDD60';
            } else {
              return '#FF6E76';
            }
          }
        }
      },
      detail: {
        fontSize: 28,
        offsetCenter: [0, '40%'],
        valueAnimation: true,
        formatter: function (value) {
          if (value > 0.75) {
            return '高'
          } else if (value > 0.5) {
            return '中'
          } else if (value > 0.25) {
            return '低'
          } else {
            return '无'
          }
        },
        color: 'inherit'
      },
      data: [
        {
          value: 0.125 + store.cognitiveLoad / 4,
        }
      ]
    }
  ]
}))
const optionVIG = computed(() => ({
  series: [
    {
      type: 'gauge',
      center: ['50%', '60%'],
      radius: '85%',
      min: 0,
      max: 1,
      splitNumber: 6,
      axisLine: {
        lineStyle: {
          width: 10,
          color: [
            [1 / 3, '#58D9F9'],
            [2 / 3, '#FDDD60'],
            [1, '#FF6E76']
          ]
        }
      },
      axisLabel: {
        color: '#fff',
        fontSize: 16,
        distance: -45,
        formatter: function (value) {
          if (Math.abs(value - 5 / 6) < 0.00001) {
            return '高';
          } else if (Math.abs(value - 0.5) < 0.00001) {
            return '中';
          } else if (Math.abs(value - 1 / 6) < 0.00001) {
            return '低';
          }
          return '';
        }
      },
      pointer: {
        itemStyle: {
          color: function (value) {
            if (value > (2 / 3)) {
              return '#7CFFB2';
            } else if (value > (1 / 3)) {
              return '#58D9F9';
            } else {
              return '#FDDD60';
            }
          }
        }
      },
      detail: {
        fontSize: 28,
        offsetCenter: [0, '40%'],
        valueAnimation: true,
        formatter: function (value) {
          if (value > (2 / 3)) {
            return '高'
          } else if (value > (1 / 3)) {
            return '中'
          } else {
            return '低'
          }
        },
        color: 'inherit'
      },
      data: [
        {
          value: store.vigilance,
        }
      ]
    }
  ]
}))
</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="charts">
        <div id="chartLeft">
          <span>认知疲劳度</span>
          <v-chart id="chartHRS" :option="optionCL" autoresize />
        </div>
        <div id="chartRight">
          <span>专注度</span>
          <v-chart id="chartSTG" :option="optionVIG" autoresize />
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