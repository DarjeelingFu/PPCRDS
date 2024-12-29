import time
from pylsl import StreamInlet, resolve_stream


# 创建接收端流的函数 
def create_inlets():
    # 尝试查找名为 "data" 的流
    print("Looking for a stream named 'data'...")
    streams = resolve_stream('name', 'data')

    # 检查是否找到了流
    if len(streams) == 0:
        raise Exception("No stream found with the name 'data'!")

    # 创建接收流
    inlet = StreamInlet(streams[0])
    return inlet


# 解析接收到的数据
def process_data(data):
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


# 接收数据并处理的函数
def receive_data(inlet):
    while True:
        # 从流中接收数据
        sample, timestamp = inlet.pull_sample()
        
        # 打印接收到的数据
        print(f"Data received at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 处理并打印数据
        process_data(sample)

        # 每3秒接收一次数据
        time.sleep(3)


if __name__ == '__main__':
    # 创建数据流接收端
    inlet = create_inlets()

    # 开始接收数据
    receive_data(inlet)
