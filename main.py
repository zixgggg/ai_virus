import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import logging
import tkinter as tk
#import requests


def check_with_ai(user_input):
    # 這裡呼叫 OpenRouter API
    # 假設回傳格式為 {"unlock": bool, "message": str}
    pass

class VirusLock:
    def __init__(self, root):
        self.root = root
#        self.root.attributes("-fullscreen", True)
#        self.root.attributes("-topmost", True) # 確保在最上層
        
        self.label = tk.Label(root, text="AI 考驗：證明你有資格使用這台電腦", font=("Courier", 20), fg="red", bg="black")
        self.label.pack(pady=50)
        
        self.entry = tk.Entry(root, font=("Courier", 18))
        self.entry.pack()
        
        self.btn = tk.Button(root, text="提交", command=self.attempt_unlock)
        self.btn.pack()

    def attempt_unlock(self):
        answer = self.entry.get()
        # 呼叫 API 判斷
        res = check_with_ai(answer) 
        
        self.label.config(text=res['message'])
        if res['unlock']:
            self.root.destroy() # 解鎖：關閉視窗

root = tk.Tk()
root.configure(bg='black')
app = VirusLock(root)
root.mainloop()
