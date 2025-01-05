<script setup>
import DataBasic from './components/DataBasic.vue'
import DataWaves from './components/DataWaves.vue'
import DataHR from './components/DataHR.vue'
import DataCamera from './components/DataCamera.vue'
import DataCognitive from './components/DataCognitive.vue'
import DataEmotionHistory from './components/DataEmotionHistory.vue'
import DataEmotion from './components/DataEmotion.vue'
import DataEEGTopography from './components/DataEEGTopography.vue'
import { useStore } from './stores'
import { onMounted, ref } from 'vue'
import io from 'socket.io-client'

const store = useStore()
const connectionState = ref(false)
const dataSource = ref('websocket')
const dialogVisible = ref(false)
const wsConfig = ref({
  host: '127.0.0.1',
  port: '8000'
})
let socket = null

function dispatch_data(data) {
  if (dataSource.value !== 'websocket') return

  if (data.hasOwnProperty('heartRate')) { store.heartRate = data.heartRate }
  if (data.hasOwnProperty('respiration')) { store.respiration = data.respiration }
  if (data.hasOwnProperty('leftEnergy')) { store.leftEnergy = data.leftEnergy }
  if (data.hasOwnProperty('ECG')) { store.ECG = data.ECG }
  if (data.hasOwnProperty('RESP')) { store.RESP = data.RESP }
  if (data.hasOwnProperty('EDA')) { store.EDA = data.EDA }
  if (data.hasOwnProperty('PULSE')) { store.PULSE = data.PULSE }
  if (data.hasOwnProperty('mean')) { store.mean = data.mean }
  if (data.hasOwnProperty('variance')) { store.variance = data.variance }
  if (data.hasOwnProperty('value')) { store.value = data.value }
  if (data.hasOwnProperty('corrdinates')) { store.corrdinates = data.corrdinates }
  if (data.hasOwnProperty('cognitiveLoad')) { store.cognitiveLoad = data.cognitiveLoad }
  if (data.hasOwnProperty('vigilance')) { store.vigilance = data.vigilance }
  if (data.hasOwnProperty('emotion')) { store.emotion = data.emotion }
  if (data.hasOwnProperty('emotionHistory')) {
    store.emotionHistory = data.emotionHistory.reduce((acc, val, idx) => {
      const colIdx = idx % 5
      if (!acc[colIdx]) acc[colIdx] = []
      acc[colIdx].push(val)
      return acc
    }, []);
  }
  if (data.hasOwnProperty('video')) { store.videoBuffer = data.video }
}

function connectWebSocket(host, port) {
  if (socket != null) {
    socket.close()
  }
  console.log('Connecting to WebSocket server:', host, port)
  socket = io('http://' + host + ':' + port, {
    reconnection: false
  })

  socket.on('connect', () => {
    console.log('WebSocket connection established')
    connectionState.value = true
  })

  socket.on('data', (msg) => {
    const data = JSON.parse(msg)
    dispatch_data(data)
  })

  socket.on('disconnect', () => {
    console.log('WebSocket connection closed')
    connectionState.value = false
  })

  socket.on('error', (err) => {
    console.log('WebSocket connection error:', err)
    connectionState.value = false
  })
}

function generateFakeDate(store) {
  // Basic
  store.heartRate = Math.floor(Math.random() * 100 + 60)
  store.respiration = Math.floor(Math.random() * 20 + 10)
  store.leftEnergy = Math.random().toFixed(2)

  // Waves
  store.ECG = Array.from({ length: 100 }, () => Math.random())
  store.RESP = Array.from({ length: 100 }, () => Math.random())
  store.EDA = Array.from({ length: 100 }, () => Math.random())
  store.PULSE = Array.from({ length: 100 }, () => Math.random())

  // Stability
  store.mean = 70 + Math.random() * 10
  store.variance = 10 + Math.random() * 5
  store.value = 70 + Math.random() * 10
  store.corrdinates = []
  for (let i = 0; i < 60; i++) {
    store.corrdinates.push([Math.random() * 10, Math.random() * 10])
  }

  // Cognitive
  store.cognitiveLoad = Math.floor(Math.random() * 4)
  store.vigilance = Math.random()

  // Emotion History
  let emotions = Array.from({ length: 30 }, () => {
    const row = Array.from({ length: 5 }, () => Math.random())
    const sum = row.reduce((acc, val) => acc + val, 0)
    return row.map(val => val / sum)
  })
  emotions = emotions[0].map((_, colIndex) => emotions.map(row => row[colIndex]))
  store.emotionHistory = emotions

  // Emotion
  let emotion = Array.from({ length: 5 }, () => Math.random());
  let maxEl = Math.max(...emotion)
  store.emotion = emotion.map(val => val / maxEl);
}

onMounted(() => {
  connectWebSocket(wsConfig.value.host, wsConfig.value.port)
  setInterval(() => {
    if (dataSource.value === 'random') {
      generateFakeDate(store)
    }
  }, 3000)
})
</script>

<template>
  <div id="header">
    <div id="headerLeftLine"></div>
    <div id="headerTitle">身心状态实时评估系统</div>
    <div id="headerRightLine"></div>
  </div>
  <div id="infoBar">
    <div id="subjectInfo">
      <span>姓名：<span>ABC</span></span>
      <span>年龄：<span>25</span></span>
      <span>实验编号：<span>1123312331</span></span>
      <span>实验时间：<span>2024.12.25</span></span> 
    </div>
    <div class="subjectInfoBorder"></div>
    <div id="status">
      <img v-if="dataSource === 'random'" src="./assets/random_data.svg" @click="dataSource = 'websocket'"/>
      <img v-if="dataSource === 'websocket'" src="./assets/receiving_data.svg" @click="dataSource = 'random'"/>
      <img v-if="connectionState === true" src="./assets/connection_established.svg" @click="dialogVisible = true"/>
      <img v-if="connectionState === false" src="./assets/connection_lost.svg" @click="dialogVisible = true"/>
    </div>
  </div>
  <div id="main">
    <div id="left" class="block">
      <div id="dataEEGTopography">
        <DataEEGTopography></DataEEGTopography>
      </div>
      <div id="dataBasic">
        <DataBasic></DataBasic>
      </div>
      <div id="dataWaves">
        <DataWaves></DataWaves>
      </div>
    </div>
    <div id="middle" class="block">
      <div id="dataCamera">
        <DataCamera></DataCamera>
      </div>
      <div id="dataCognitive">
        <DataCognitive></DataCognitive>
      </div>
    </div>
    <div id="right" class="block">
      <div id="dataHR">
        <DataHR></DataHR>
      </div>
      <div id="dataEmotionHistory">
        <DataEmotionHistory></DataEmotionHistory>
      </div>
      <div id="dataEmotion">
        <DataEmotion></DataEmotion>
      </div>
    </div>
  </div>

  <el-dialog v-model="dialogVisible" title="WebSocket配置" width="300">
    <el-form :model="wsConfig">
      <el-form-item label="地址">
        <el-input v-model="wsConfig.host"/>
      </el-form-item>
      <el-form-item label="端口">
        <el-input v-model="wsConfig.port"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="connectWebSocket(wsConfig.host, wsConfig.port), dialogVisible = false">
          连接
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
/* h50px */
#header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 10px 0;
  height: 30px;
}

#headerTitle {
  text-align: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  margin: 0 20px;
}

#headerLeftLine,
#headerRightLine {
  flex: 1;
  height: 3px;
  background-color: aquamarine;
}

#infoBar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 30px;
  margin: 0 20px;
  width: calc(100% - 40px);
  position: relative;
}

/* h40px */
#subjectInfo {
  color: white;
  font-size: 18px;
  padding: 0 10px;
  margin-left: 30px;
  height: 100%;
  width: 50%;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;

  /* border: 1px solid aquamarine;
  border-bottom: none;
  box-sizing: border-box; */
}

.subjectInfoBorder {
  position: absolute;
  height: 100%;
  width: calc(60% + 20px);

  border: 1px solid aquamarine;
  border-bottom: none;
  box-sizing: border-box;

  transform: perspective(500px) rotateX(30deg) translate(0.9%, 0) scale(1, 1.2);
}

#status {
  height: 100%;
  border: 1px solid aquamarine;
  border-bottom: none;
  box-sizing: border-box;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

#status img {
  width: 16px;
  margin: 0 5px;
}

#main {
  position: relative;
  height: calc(100vh - 90px);
  margin: 0 20px;

  display: flex;
  justify-content: space-between;

  border: 1px solid aquamarine;
  box-sizing: border-box;
}

#left #right #middle {
  height: 100%;
  box-sizing: border-box;
}

#left {
  width: 30%;
  border-right: 1px solid aquamarine;
}

#middle {
  width: 40%;
  border-right: 1px solid aquamarine;
}

#right {
  width: 30%
}

#dataEEGTopography,
#dataBasic {
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataEEGTopography {
  height: 33%;
}

#dataBasic {
  height: 33%;
}

#dataWaves {
  height: 34%;
}

#dataCamera {
  height: 66%;
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataCognitive {
  height: 34%;
}

#dataHR,
#dataEmotionHistory {
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataHR {
  height: 33%;
}

#dataEmotionHistory {
  height: 33%;
}

#dataEmotion {
  height: 34%;
}
</style>
