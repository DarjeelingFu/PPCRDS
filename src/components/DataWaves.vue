<script setup>
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import VChart, { THEME_KEY } from 'vue-echarts'
import { provide, computed } from 'vue'
import { useStore } from '../stores'

provide(THEME_KEY, 'dark')
use([GridComponent, LineChart, CanvasRenderer])
const store = useStore()

const optionECG = computed(() => ({
  xAxis: {
    show: true,
    type: 'category',
    data: Array.from({ length: store.ECG.length }, (_, i) => i),
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true,
    },
    name: '心电',
    nameLocation: 'middle', // Position the title in the middle
    nameTextStyle: {
      fontSize: 12,
      padding: [-10, 0, 0, 0] // Adjust padding if needed
    }
  },
  yAxis: {
    show: true,
    type: 'value',
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true
    },
  },
  series: [
    {
      data: store.ECG,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 1
      }
    }
  ],
  grid: {
    show: false,
    left: '5%',
    right: '5%',
    top: '5%',
    bottom: '20%',
    containLabel: true
  }
}))
const optionRESP = computed(() => ({
  xAxis: {
    show: true,
    type: 'category',
    data: Array.from({ length: store.RESP.length }, (_, i) => i),
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true,
    },
    name: '呼吸',
    nameLocation: 'middle', // Position the title in the middle
    nameTextStyle: {
      fontSize: 12,
      padding: [-10, 0, 0, 0] // Adjust padding if needed
    }
  },
  yAxis: {
    show: true,
    type: 'value',
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true
    }
  },
  series: [
    {
      data: store.RESP,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 1
      }
    }
  ],
  grid: {
    show: false,
    left: '5%',
    right: '5%',
    top: '5%',
    bottom: '20%',
    containLabel: true
  }
}))
const optionEDA = computed(() => ({
  xAxis: {
    show: true,
    type: 'category',
    data: Array.from({ length: store.EDA.length }, (_, i) => i),
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true,
    },
    name: '皮电',
    nameLocation: 'middle', // Position the title in the middle
    nameTextStyle: {
      fontSize: 12,
      padding: [-10, 0, 0, 0] // Adjust padding if needed
    }
  },
  yAxis: {
    show: true,
    type: 'value',
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true
    }
  },
  series: [
    {
      data: store.EDA,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 1
      }
    }
  ],
  grid: {
    show: false,
    left: '5%',
    right: '5%',
    top: '5%',
    bottom: '20%',
    containLabel: true
  }
}))
const optionP = computed(() => ({
  xAxis: {
    show: true,
    type: 'category',
    data: Array.from({ length: store.PULSE.length }, (_, i) => i),
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true,
    },
    name: '脉搏',
    nameLocation: 'middle', // Position the title in the middle
    nameTextStyle: {
      fontSize: 12,
      padding: [-10, 0, 0, 0] // Adjust padding if needed
    }
  },
  yAxis: {
    show: true,
    type: 'value',
    axisTick: {
      show: false
    },
    splitLine: {
      show: false
    },
    axisLabel: {
      show: false
    },
    axisLine: {
      show: true
    }
  },
  series: [
    {
      data: store.PULSE,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 1
      }
    }
  ],
  grid: {
    show: false,
    left: '5%',
    right: '5%',
    top: '5%',
    bottom: '20%',
    containLabel: true
  }
}))

</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="title">波形图</div>
      <div id="charts">
        <div id="chartR1">
          <v-chart id="chartHR" :option="optionECG" autoresize />
          <v-chart id="chartHR" :option="optionRESP" autoresize />
        </div>
        <div id="chartR2">
          <v-chart id="chartHR" :option="optionEDA" autoresize />
          <v-chart id="chartHR" :option="optionP" autoresize />
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
  flex-direction: column;
  justify-content: space-around;
  height: calc(100% - 30px);
}

#chartR1,
#chartR2 {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: calc((100% - 30px) * 0.5);
}
</style>