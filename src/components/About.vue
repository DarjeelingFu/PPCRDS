<script setup>
import { Notivue, push } from 'notivue'
</script>

<template>
  <div id="aboutContainer">
    <div class="flexRow" id="alertContainer">
      <!-- <div id="alert">
        By modifying the codes of this project you admit that you are turning these epic codes into bull shits. My codes are elegant, yours are not.
      </div> -->
      <div id="alert">
        <img src="../assets/notice.png" alt="By modifying the codes of this project you admit that you are turning these epic codes into bull shits. My codes are elegant, yours are not." />
      </div>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');

#aboutContainer {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100vh;
  position: relative;
  background-color: rgb(255, 255, 255);
  box-shadow: inset 0 0 300px 3px rgba(255, 255, 255, 0.151);
  z-index: -1;
}

#aboutContainer::before {
  content: "";
  width: 50%;
  height: 70vh;
  position: absolute;
  left: 0;
  bottom: 0;
  background-image: url('../assets/mygo.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-size: 50%;
  z-index: -1;
}

#aboutContainer::after {
  content: "";
  width: 50%;
  height: 70vh;
  position: absolute;
  right: 0;
  bottom: 0;
  background-image: url('../assets/ave_mujica.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-size: 50%;
  z-index: -1;
}

.flexRow {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

#alertContainer {
  width: 100%;
  height: 100%;
}

#alert {
  font-size: 36px;
  text-align: center;
  padding: 20px;
  background: linear-gradient(to right, #03d9ff, #ff00c8);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;

  width: 75%;
  padding-bottom: 40vh;

  font-family: 'Permanent Marker', cursive
}

</style>