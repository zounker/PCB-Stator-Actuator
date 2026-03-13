# AI-Powered High-Precision PCB Axial Flux Motor Development

![Status](https://img.shields.io/badge/Status-A--Sample%20Testing-blue)
![AI-Powered](https://img.shields.io/badge/AI--Integration-Cloud%20%2B%20Edge-green)

本專案致力於研發基於 PCB 定子技術的新世代高精度軸向伺服電機 (PCB Stator Actuator)，並全面導入端到端 AI 協作流程。

## 🚀 核心開發理念：雙引擎 AI 架構
本計畫不只是硬體研發，更是 AI 落地應用的實踐：
1. **雲端生成式 AI (Gemini) 研發賦能：** 作為「虛擬協同開發夥伴」，輔助進行 KiCAD 電路佈局設計、Fusion360 參數化建模與測試腳本自動化生成，縮短 40% 以上的研發週期。
2. **邊緣分析式 AI (TinyML) 智能驅動：** 規劃採用 STM32G431 + STM32Cube.AI 工具鏈，將 BEMF 數據轉化為量化 (INT8) 模型，實現主動轉矩補償與預測性維護。

## 📂 專案內容
- **/tools**: 包含與 Gemini 協同開發的 BEMF 測試數據擷取腳本 `bemf_logger.py`。
- **/docs**: 研發設計思路與 AI 協作過程紀錄 (脫敏版)。
- **/firmware**: 基於 B-G431B-ESC1 的驅動開發藍圖 (預計導入 TinyML)。

## 📈 目前進度
- [x] 核心機電拓撲設計 (Cloud AI 協助)
- [x] A-Sample 性能樣品製造
- [x] BEMF 性能數據採集與驗證 (進行中)
- [ ] TinyML 模型訓練與邊緣端部署 (計畫中)

## 🛠️ 開發工具
- **Hardware Design:** Fusion 360, KiCAD
- **AI Tools:** Google Gemini (Cloud), STM32Cube.AI (Edge)
- **Embedded:** STM32G431 (Cortex-M4), AS5047P Encoder

## ⚖️ License
This project uses non-confidential scripts for open community sharing. Core hardware designs are under patent pending.
