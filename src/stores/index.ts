import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => ({
    // Basic
    heartRate: 70,
    respiration: 20,
    leftEnergy: 0.2,

    // Waves
    ECG: [],
    RESP: [],
    EDA: [],
    PULSE: [],

    // Stability
    mean: 70,
    variance: 10,
    value: 70,

    corrdinates: [],

    // Camera
    videoBuffer: null,

    // Cognitive
    cognitiveLoad: 0,
    vigilance: 0,

    // Emotion History
    emotionHistory: [],

    // Emotion
    emotion: [],

    // EEG topography
    topography: [],

    // Camera Video Stream Url
    videoSrc: 'http://127.0.0.1:8000/video_feed'
  })
})