<script setup>
import { onMounted, ref } from 'vue';

const logs = ref([])
function addLog(content) {
  logs.value.push({
    time: new Date().toLocaleTimeString(),
    content: content
  });

  if (logs.value.length > 10) {
    logs.value.shift();
  }
}

onMounted(() => {
  setInterval(() => {
    addLog('通过xx模态检测到xx情绪');
  }, 3000);
});
</script>

<template>
  <div id="container">
    <div id="panel">
      <div id="logger">
        <div v-for="log in logs" :key="log.time">
          <span id="loggerTime">[{{ log.time }}] </span>
          <span id="loggerContent">{{ log.content }}</span>
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
  width: calc(100% - 40px);
  height: calc(100% - 40px);
  background: #100b2b;
  border-radius: 5px;
  margin: 5px;
  padding: 15px;
}

#logger {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: white;
}

#logger::-webkit-scrollbar {
  display: none;
}

#logger span {
  word-wrap: break-word;
}

#loggerTime {
  color: aquamarine;
}

#loggerContent {
  color: rgb(226, 226, 226);
}
</style>