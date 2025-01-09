import time
from pylsl import StreamInlet, resolve_stream


# 创建接收端流的函数 
def create_inlets_EEG():
    # 尝试查找名为 "data" 的流
    print("Looking for a stream named 'data'...")
    streams = resolve_stream('type', 'EEG_process')

    # 检查是否找到了流
    if len(streams) == 0:
        raise Exception("No stream found with the name 'EEG'!")

    # 创建接收流
    inlet = StreamInlet(streams[0])
    return inlet

def create_inlets_ECG():
    # 尝试查找名为 "data" 的流
    print("Looking for a stream named 'data'...")
    streams = resolve_stream('type', 'ECG_process')

    # 检查是否找到了流
    if len(streams) == 0:
        raise Exception("No stream found with the name 'ECG'!")

    # 创建接收流
    inlet = StreamInlet(streams[0])
    return inlet

if __name__ == '__main__':
    inlet1 = create_inlets_EEG()
    inlet2 = create_inlets_ECG()

    while True:
        sample1, _ = inlet1.pull_sample()        
        sample2, _ = inlet2.pull_sample()
        print("EEG data:", sample1)
        print("ECG data:", sample2)

        