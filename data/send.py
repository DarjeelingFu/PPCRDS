import time
import random
import numpy as np
from pylsl import StreamInfo, StreamOutlet

# 数据流定义
def create_streams():
    info = StreamInfo('data', 'EEG', 24283, 200, 'float32', 'data')
    outlet = StreamOutlet(info)

    return outlet


# 模拟数据生成
def generate_data():
    # A: 心率，呼吸，剩余体能
    heart_rate = random.uniform(60, 100)
    respiration = random.uniform(12, 20)
    fitness = random.uniform(50, 100)

    # B: 心电，呼吸电，皮电，脉搏电，每个信号 6000 个数据点，总共 4 个信号 (4, 6000)
    ecg = np.random.randn(6000)  # 模拟心电数据
    respiration_electro = np.random.randn(6000)  # 模拟呼吸电数据
    skin_conductance = np.random.randn(6000)  # 模拟皮电数据
    pulse = np.random.randn(6000)  # 模拟脉搏电数据
    data_B = np.array([ecg, respiration_electro, skin_conductance, pulse])  # 生成 (4, 6000) 的 ndarray

    # 将 data_B 展平为 1D 数组，长度为 24000
    data_B_flat = data_B.flatten()  # 这里是将 (4, 6000) 展平成一个长度为 24000 的数组

    # C: 正态分布均值，方差，正态分布值
    mean = random.uniform(0, 10)
    variance = random.uniform(0, 5)
    normal_value = random.gauss(mean, variance)

    # D: 60个二维坐标
    coordinates = np.random.uniform(-100, 100, 120)  # 60个二维坐标

    # E: 认知疲劳度
    cognitive_fatigue = random.uniform(0, 100)

    # F: 专注度
    focus_level = random.uniform(0, 100)

    # G: 五个情绪识别概率
    emotion_probs = np.random.dirichlet(np.ones(5))  # 五个情绪识别的概率，和为1

    # H: 过去30s五个情绪识别的概率（每秒一个结果，总共30秒），最后五个结果与G相同
    past_emotion_probs = np.array([np.random.dirichlet(np.ones(5)) for _ in range(30)])  # 过去30秒的情绪识别概率
    past_emotion_probs[-1:] = emotion_probs  # 最后的五个结果与当前的情绪识别概率一致

    return ([heart_rate, respiration, fitness, list(data_B_flat.flatten()), mean, variance, normal_value, list(coordinates.flatten()), cognitive_fatigue, focus_level, list(emotion_probs.flatten()), list(past_emotion_probs.flatten())])


# 数据发送函数
def send_data(outlets):
    outlet = outlets
    while True:
        # 生成数据
        data = generate_data()
        data = data[:3] + data[3] + data[4:7]+data[7]+data[8:10]+data[10]+data[11]

        # 发送数据
        outlet.push_sample(data)

        # 打印发送的数据
        print("Data sent at: ", time.strftime('%Y-%m-%d %H:%M:%S'))
        print(f"A (Heart rate, Respiration, Fitness): {data[0:2]}")
        print(f"B (ECG, Respiration Electro, Skin Conductance, Pulse): {data[3:12]}... (First 10 values)")
        print(f"C (Normal Dist Mean, Variance, Normal Value): {data[24003:24005]}")
        print(f"D (Coordinates): {data[24006:24015]}... (First 10 values)")
        print(f"E (Cognitive Fatigue): {data[24126]}")
        print(f"F (Focus Level): {data[24127]}")
        print(f"G (Emotion Probabilities): {data[24128:24132]}")
        print(f"H (Past Emotion Probabilities): {data[24278:24282]}... (Last 5 values)")  # 打印过去30秒的前10个结果

        # 每3秒发送一次数据
        time.sleep(3)


if __name__ == '__main__':
    # 创建数据流
    outlets = create_streams()

    # 开始发送数据
    send_data(outlets)
