import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import webbrowser
import os
import time

developer_root = None

# 更新不再询问的时间戳
def update_dont_ask_again():
    with open("time_setting.txt", "w") as f:
        f.write(str(time.time()))

# 检查是否需要显示不再询问的选项
def should_ask_again():
    if not os.path.exists("time_setting.txt"):
        return True
    with open("time_setting.txt", "r") as f:
        last_ask_time = float(f.read().strip())
    return time.time() - last_ask_time > 86400  # 86400 seconds in 24 hours

# 重置弹窗时间（删除时间设置文件）
def reset_time():
    try:
        if os.path.exists("time_setting.txt"):
            os.remove("time_setting.txt")
            messagebox.showinfo("成功", "弹窗时间已重置。")
        else:
            messagebox.showinfo("提示", "时间戳文件不存在，无需重置。")
    except Exception as e:
        messagebox.showerror("错误", f"重置时间时发生错误：{e}")

# 复制链接到剪贴板
def on_copy():
    root.clipboard_clear()
    root.clipboard_append(result_text.get('1.0', tk.END))
    messagebox.showinfo("成功", "链接已复制到剪贴板。")

# 修改链接
def modify_link():
    original_url = url_entry.get()
    if original_url == "#*#*vistamin*#*#":  # 特定条件触发开发者模式界面
        open_developer_mode_interface()
        return

    try:
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)

        # 修改参数
        query_params['contentType'] = ['x_url']
        query_params['catalogType'] = ['elecedu']

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query_string,
            parsed_url.fragment
        ))

        result_text.config(state=NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, new_url)
        result_text.config(state=DISABLED)

        # 检查是否自动打开浏览器
        if auto_open_var.get():
            webbrowser.open(new_url, new=2)  # 使用新标签页打开链接
        elif should_ask_again():
            response = messagebox.askyesno("打开浏览器", "是否立即在浏览器中打开新链接？")
            if response:
                webbrowser.open(new_url, new=2)
            if not response:
                do_not_show_again_var.set(True)
                update_dont_ask_again()

    except Exception as e:
        messagebox.showerror("错误", f"修改链接时发生错误：{e}")

# 开发者模式界面
def open_developer_mode_interface():
    global developer_root
    if developer_root is None:
        developer_root = ttk.Toplevel(root)
        developer_root.title("开发者模式")
        reset_button = ttk.Button(developer_root, text="重置弹窗时间", command=reset_time, style='info.TButton')
        reset_button.pack(pady=10)
        exit_dev_mode_button = ttk.Button(developer_root, text="退出开发者模式", command=exit_developer_mode, style='warning.TButton')
        exit_dev_mode_button.pack(pady=10)

def exit_developer_mode():
    global developer_root
    if developer_root:
        developer_root.destroy()
        developer_root = None

# 创建主窗口
root = ttk.Window(themename="litera")
root.title("国家中小学智慧教育平台Downtool --by vistamin")
root.geometry("800x600")

# 创建主框架
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=BOTH, expand=YES)

# 创建输入框
url_label = ttk.Label(main_frame, text="请输入原始链接：")
url_label.pack(fill=X)
url_entry = ttk.Entry(main_frame, width=70)
url_entry.pack(fill=X, pady=10)

# 创建修改链接按钮
modify_button = ttk.Button(main_frame, text="修改链接", command=modify_link, style='primary.TButton')
modify_button.pack(fill=X, pady=10)

# 创建文本控件显示修改后的链接
result_text = tk.Text(main_frame, width=70, height=5, state=DISABLED)
result_text.pack(fill=BOTH, expand=YES, pady=10)

# 创建复制链接按钮
copy_button = ttk.Button(main_frame, text="复制链接", command=on_copy, style='info.TButton')
copy_button.pack(fill=X, pady=10)

# 创建自动打开浏览器的复选框
auto_open_var = tk.BooleanVar()
auto_open_checkbox = ttk.Checkbutton(main_frame, text="生成链接后自动打开浏览器", variable=auto_open_var)
auto_open_checkbox.pack(fill=X)

# 创建不再询问的复选框
do_not_show_again_var = tk.BooleanVar()
do_not_show_again_checkbox = ttk.Checkbutton(main_frame, text="24小时内不再询问", variable=do_not_show_again_var)
do_not_show_again_checkbox.pack(fill=X)

# 主循环
root.mainloop()
