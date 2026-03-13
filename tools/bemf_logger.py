使用方法 (Usage)
連接硬體模式：
code
Bash
python bemf_logger.py --port COM3 --baud 115200
無硬體模擬模式 (展示用)：
code
Bash
python bemf_logger.py --mock
code
Code
---

### 第二步：上傳 Python 程式碼 `bemf_logger.py`
*（在您的 GitHub 專案中新增一個檔案名為 `bemf_logger.py`，並貼上以下由 Gemini 輔助生成的程式碼）*

```python
import serial
import time
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================
# BEMF Data Logger & Visualizer
# Co-developed by PCB Stator Actuator Team & Agentic AI
# ==========================================

class BEMFLogger:
    def __init__(self, port, baudrate, mock_mode=False):
        self.mock_mode = mock_mode
        self.port = port
        self.baudrate = baudrate
        self.data_buffer = {'time':[], 'phase_a': [], 'phase_b': [], 'phase_c':[]}
        self.start_time = time.time()
        self.is_logging = True

        if not self.mock_mode:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"[*] Successfully connected to {self.port} at {self.baudrate} bps.")
            except Exception as e:
                print(f"[!] Error connecting to serial port: {e}")
                print("[*] Falling back to Mock Mode...")
                self.mock_mode = True

    def read_data(self):
        """讀取 BEMF 數據 (支援真實硬體與模擬模式)"""
        current_time = time.time() - self.start_time
        
        if self.mock_mode:
            # 模擬平滑的 BEMF 正弦波 (無專利機密，僅為基礎物理數學模型)
            # 模擬完美的 120 度相位差，展示「極致平順」的預期效果
            freq = 5.0 # 模擬 5Hz 轉速
            phase_a = np.sin(2 * np.pi * freq * current_time) * 5.0
            phase_b = np.sin(2 * np.pi * freq * current_time - (2*np.pi/3)) * 5.0
            phase_c = np.sin(2 * np.pi * freq * current_time + (2*np.pi/3)) * 5.0
            time.sleep(0.02) # 模擬 UART 延遲
            return current_time, phase_a, phase_b, phase_c
        else:
            # 讀取真實微控制器 (如 B-G431B-ESC1) 傳來的 CSV 格式字串: "time,Va,Vb,Vc\n"
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    vals = line.split(',')
                    if len(vals) == 4:
                        return float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3])
                except Exception:
                    pass
        return None, None, None, None

    def update_plot(self, frame, lines, ax):
        """即時更新 Matplotlib 圖表"""
        t, va, vb, vc = self.read_data()
        
        if t is not None:
            self.data_buffer['time'].append(t)
            self.data_buffer['phase_a'].append(va)
            self.data_buffer['phase_b'].append(vb)
            self.data_buffer['phase_c'].append(vc)

            # 保持畫面只顯示最新的 100 筆數據
            if len(self.data_buffer['time']) > 100:
                for key in self.data_buffer:
                    self.data_buffer[key] = self.data_buffer[key][-100:]

            lines[0].set_data(self.data_buffer['time'], self.data_buffer['phase_a'])
            lines[1].set_data(self.data_buffer['time'], self.data_buffer['phase_b'])
            lines[2].set_data(self.data_buffer['time'], self.data_buffer['phase_c'])
            
            ax.relim()
            ax.autoscale_view()
            
            # 動態平移 X 軸
            if t > 2.0:
                ax.set_xlim(t - 2.0, t + 0.1)

        return lines

    def run_visualization(self):
        """啟動視覺化視窗"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Real-time BEMF Waveform (Preparing for TinyML Dataset)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.grid(True)

        lines = [
            ax.plot([],[], 'r-', label='Phase A')[0],
            ax.plot([], [], 'g-', label='Phase B')[0],
            ax.plot([], [], 'b-', label='Phase C')[0]
        ]
        ax.legend(loc="upper right")
        ax.set_xlim(0, 2)
        ax.set_ylim(-6, 6)

        print("[*] Starting visualization. Close the window to save data and exit.")
        
        ani = FuncAnimation(fig, self.update_plot, fargs=(lines, ax), interval=20, cache_frame_data=False)
        plt.show()
        
        self.save_to_csv()

    def save_to_csv(self):
        """將數據存檔，作為未來訓練 TinyML 邊緣運算模型的 Dataset"""
        filename = f"bemf_dataset_{int(time.time())}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'PhaseA_V', 'PhaseB_V', 'PhaseC_V'])
            for i in range(len(self.data_buffer['time'])):
                writer.writerow([
                    self.data_buffer['time'][i],
                    self.data_buffer['phase_a'][i],
                    self.data_buffer['phase_b'][i],
                    self.data_buffer['phase_c'][i]
                ])
        print(f"[*] Data saved to {filename}. Ready for TinyML INT8 Quantization.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BEMF Data Logger for PCB Motor")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port (e.g., COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without hardware")
    args = parser.parse_args()

    logger = BEMFLogger(port=args.port, baudrate=args.baud, mock_mode=args.mock)
    logger.run_visualization()
