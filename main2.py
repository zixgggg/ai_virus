import tkinter as tk
from tkinter import scrolledtext
import threading
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# 1. 設定你的 API 客戶端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("openrouter_api_key"), 
)

class VirusLock:
    def __init__(self, root):
        self.root = root
        self.root.title("AI SYSTEM LOCK")
        #self.root.attributes("-fullscreen", True) # 全螢幕鎖定
        #self.root.attributes("-topmost", True)   # 始終置頂
        self.root.configure(bg="#0a0a0a")        # 深黑色背景

        # 紀錄對話歷史，讓 AI 記得你前面說過什麼
        self.messages = [
            {"role": "system", "content": "你是一個佔據使用者電腦的瘋狂 AI。你必須與使用者玩一個猜謎或邏輯遊戲。回傳 JSON 格式：{'unlock': bool, 'reply': str}。除非使用者讓你非常滿意，否則 unlock 永遠為 false。你可以隨時耍賴不解鎖，並在 reply 裡嘲諷他。"}
        ]

        self.setup_ui()

    def setup_ui(self):
        # 標題
        self.title_label = tk.Label(
            self.root, text="[ 系統已遭 AI 接管 ]", 
            font=("Courier New", 30, "bold"), fg="#ff0000", bg="#0a0a0a"
        )
        self.title_label.pack(pady=20)

        # 聊天室記錄區 (ScrolledText)
        self.chat_display = scrolledtext.ScrolledText(
            self.root, font=("Consolas", 14), bg="#1a1a1a", fg="#00ff00",
            state='disabled', width=100, height=25, borderwidth=0
        )
        self.chat_display.pack(pady=10, padx=50)

        # 輸入區域容器
        input_frame = tk.Frame(self.root, bg="#0a0a0a")
        input_frame.pack(fill="x", side="bottom", padx=50, pady=50)

        # 輸入框 (Entry)
        self.user_input = tk.Entry(
            input_frame, font=("Consolas", 18), bg="#222", fg="white", 
            insertbackground="white", borderwidth=2
        )
        self.user_input.pack(side="left", fill="x", expand=True, ipady=10)
        self.user_input.bind("<Return>", lambda e: self.process_input()) # 綁定 Enter 鍵
        self.user_input.focus_set() # 自動聚焦到輸入框

        # 發送按鈕
        self.send_btn = tk.Button(
            input_frame, text="傳送", command=self.process_input,
            bg="#333", fg="white", font=("Arial", 12), width=10
        )
        self.send_btn.pack(side="right", padx=10)

        self.append_chat("AI", "嘿... 你的電腦現在歸我管了。想拿回去？先陪我玩個遊戲吧。")

    def append_chat(self, sender, text):
        """將訊息顯示在聊天室窗口"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {text}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END) # 自動滾動到底部

    def process_input(self):
        content = self.user_input.get().strip()
        if not content: return

        self.append_chat("你", content)
        self.user_input.delete(0, tk.END) # 清空輸入框
        
        # 啟動 Thread 呼叫 API，避免 UI 畫面卡住
        threading.Thread(target=self.get_ai_response, args=(content,), daemon=True).start()

    def get_ai_response(self, text):
        try:
            self.messages.append({"role": "user", "content": text})
            
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-001",
                messages=self.messages,
                response_format={"type": "json_object"}
            )

            res_data = json.loads(response.choices[0].message.content)
            reply = res_data.get("reply", "...")
            can_unlock = res_data.get("unlock", False)

            self.messages.append({"role": "assistant", "content": reply})
            
            # 回到主執行緒更新 UI
            self.root.after(0, lambda: self.append_chat("AI", reply))

            if can_unlock:
                self.root.after(2000, self.root.destroy) # 兩秒後解鎖

        except Exception as e:
            self.root.after(0, lambda: self.append_chat("系統錯誤", str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusLock(root)
    root.mainloop()
