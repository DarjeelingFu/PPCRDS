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
    emotion: []
  })
})