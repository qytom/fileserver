#!/usr/bin/env python3
import sys
import os
import threading
import socket
import http.server
import socketserver
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fileserver.log')
)
logger = logging.getLogger(__name__)

# 全局变量用于存储服务器信息
server_info = {'running': False, 'error': None, 'httpd': None, 'thread': None}

# Android权限请求函数
def check_android_permissions():
    """检查并请求Android存储权限"""
    if 'ANDROID_ARGUMENT' not in os.environ:
        return True
    
    try:
        from jnius import autoclass, cast
        from android import activity
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        
        # 检查权限
        ContextCompat = autoclass('androidx.core.content.ContextCompat')
        Manifest = autoclass('android.Manifest$permission')
        
        # 检查多个存储权限
        permissions = [
            Manifest.READ_EXTERNAL_STORAGE,
            Manifest.WRITE_EXTERNAL_STORAGE
        ]
        
        # 检查所有权限
        all_granted = True
        for perm in permissions:
            result = ContextCompat.checkSelfPermission(currentActivity, perm)
            if result != 0:  # PackageManager.PERMISSION_GRANTED
                all_granted = False
                break
        
        # 所有权限已授予
        if all_granted:
            logger.info("存储权限已授予")
            return True
        
        # 请求权限
        logger.info("请求存储权限...")
        ActivityCompat = autoclass('androidx.core.app.ActivityCompat')
        ActivityCompat.requestPermissions(currentActivity, permissions, 0)
        
        # 等待用户响应
        import time
        time.sleep(3)  # 给用户时间授予权限
        
        # 再次检查权限
        all_granted = True
        for perm in permissions:
            result = ContextCompat.checkSelfPermission(currentActivity, perm)
            if result != 0:
                all_granted = False
                break
        
        if all_granted:
            logger.info("存储权限已授予")
            return True
        else:
            logger.warning("存储权限未授予")
            return False
    except Exception as e:
        logger.error(f"权限检查失败: {e}")
        return False  # 如果出错，返回False，避免无权限访问

def detect_available_directories():
    """检测所有可用的目录"""
    available_dirs = []
    
    # Android: 尝试多个可能的目录
    if 'ANDROID_ARGUMENT' in os.environ:
        # 扩展可能的目录列表
        possible_dirs = [
            # 应用私有目录
            os.environ.get('ANDROID_APP_PATH', ''),
            os.environ.get('ANDROID_PRIVATE', ''),
            os.environ.get('ANDROID_UNPACK', ''),
            # 应用数据目录
            '/data/data/org.example.fileserver/files',
            '/data/data/org.example.fileserver/app',
            # 外部存储
            '/sdcard',
            '/sdcard/Download',
            '/sdcard/Downloads',
            '/sdcard/DCIM',
            '/sdcard/Pictures',
            '/sdcard/Music',
            '/storage/emulated/0',
            '/storage/emulated/0/Download',
            '/storage/emulated/0/Downloads',
            '/storage/emulated/0/DCIM',
            '/storage/emulated/0/Pictures',
            '/storage/emulated/0/Music',
            '/storage/self/primary',
            '/storage/self/primary/Download',
            '/storage/self/primary/DCIM',
            '/storage/self/primary/Pictures',
            '/storage/self/primary/Music',
            # 临时目录
            '/data/local/tmp',
            '/tmp',
        ]
        
        # 尝试每个目录
        for d in possible_dirs:
            if d and os.path.exists(d):
                try:
                    test_file = os.path.join(d, '.test_write')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    available_dirs.append(d)
                    logger.debug(f"目录可用: {d}")
                except Exception as e:
                    logger.debug(f"目录 {d} 不可用: {e}")
                    continue
        
        # 如果都不行，创建并使用files子目录
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            files_dir = os.path.join(current_dir, 'files')
            os.makedirs(files_dir, exist_ok=True)
            # 测试写入
            test_file = os.path.join(files_dir, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            available_dirs.append(files_dir)
            logger.debug(f"files目录可用: {files_dir}")
        except Exception as e:
            logger.error(f"无法创建files目录: {e}")
        
        # 最后尝试当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        available_dirs.append(current_dir)
        logger.debug(f"当前目录: {current_dir}")
    else:
        # Windows/Linux: 使用Downloads目录
        downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        if os.path.exists(downloads):
            available_dirs.append(downloads)
        
        # 添加桌面目录
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if os.path.exists(desktop):
            available_dirs.append(desktop)
        
        # 添加文档目录
        documents = os.path.join(os.path.expanduser('~'), 'Documents')
        if os.path.exists(documents):
            available_dirs.append(documents)
        
        # 最后添加当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        available_dirs.append(current_dir)
    
    # 去重并返回
    return list(set(available_dirs))

def get_app_directory():
    """获取默认应用目录"""
    available_dirs = detect_available_directories()
    if available_dirs:
        logger.info(f"使用默认目录: {available_dirs[0]}")
        return available_dirs[0]
    
    # 最后尝试当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"使用当前目录: {current_dir}")
    return current_dir

APP_DIR = get_app_directory()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"获取本地IP失败: {e}")
        return '127.0.0.1'

def is_port_available(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.close()
        return True
    except Exception as e:
        logger.warning(f"端口 {port} 不可用: {e}")
        return False

def get_available_port(start_port=8000, max_attempts=10):
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port):
            logger.info(f"找到可用端口: {port}")
            return port
    logger.error("无法找到可用端口")
    return None

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # 设置更大的缓冲区大小 (4MB)
    buffer_size = 4 * 1024 * 1024
    
    def do_GET(self):
        """处理GET请求，支持断点续传"""
        try:
            logger.info(f"收到请求: {self.path}")
            logger.info(f"当前工作目录: {os.getcwd()}")
            
            if not os.path.exists(os.getcwd()):
                logger.error(f"错误: 当前目录不存在: {os.getcwd()}")
                self.send_error(404, "Directory not found")
                return
            
            # 处理断点续传
            if self.path != '/' and os.path.isfile(self.path[1:]):
                return self.handle_file_request()
            
            super().do_GET()
        except Exception as e:
            logger.error(f"处理请求时出错: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_file_request(self):
        """处理文件请求，支持断点续传"""
        file_path = self.path[1:]
        
        try:
            file_size = os.path.getsize(file_path)
            range_header = self.headers.get('Range', None)
            
            if range_header:
                # 处理断点续传
                range_value = range_header.split('=')[1]
                start, end = range_value.split('-')
                start = int(start)
                end = int(end) if end else file_size - 1
                
                if start >= file_size:
                    self.send_error(416, "Requested range not satisfiable")
                    return
                
                # 发送部分内容
                self.send_response(206)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(end - start + 1))
                self.send_header('Content-Type', self.guess_type(file_path))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Connection', 'keep-alive')
                self.end_headers()
                
                # 发送文件内容
                with open(file_path, 'rb') as f:
                    f.seek(start)
                    remaining = end - start + 1
                    while remaining > 0:
                        chunk_size = min(self.buffer_size, remaining)
                        buf = f.read(chunk_size)
                        if not buf:
                            break
                        self.wfile.write(buf)
                        self.wfile.flush()
                        remaining -= chunk_size
            else:
                # 发送完整文件
                self.send_response(200)
                self.send_header('Content-Type', self.guess_type(file_path))
                self.send_header('Content-Length', str(file_size))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Connection', 'keep-alive')
                self.end_headers()
                
                # 发送文件内容
                with open(file_path, 'rb') as f:
                    while True:
                        buf = f.read(self.buffer_size)
                        if not buf:
                            break
                        self.wfile.write(buf)
                        self.wfile.flush()
        except Exception as e:
            logger.error(f"处理文件请求时出错: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def list_directory(self, path):
        """重写列表目录方法，支持中文显示和文件大小格式化"""
        try:
            import datetime
            import urllib.parse
            import mimetypes
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>文件服务器</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                h1 {{ color: #333; text-align: center; }}
                .header {{ background-color: #3498db; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #2c3e50; color: white; font-weight: bold; }}
                tr:hover {{ background-color: #f8f9fa; }}
                a {{ color: #3498db; text-decoration: none; font-weight: 500; }}
                a:hover {{ text-decoration: underline; color: #2980b9; }}
                .size {{ text-align: right; font-family: monospace; }}
                .type {{ width: 100px; }}
                .time {{ width: 180px; }}
                .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 14px; }}
                .dir-icon {{ color: #f39c12; }}
                .file-icon {{ color: #3498db; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 文件服务器</h1>
                <p>当前目录: {path}</p>
            </div>
            <table>
                <tr>
                    <th>类型</th>
                    <th>文件名</th>
                    <th class="size">大小</th>
                    <th class="time">修改时间</th>
                </tr>
                <tr>
                    <td><span class="dir-icon">📁</span></td>
                    <td><a href="../">../</a></td>
                    <td class="size"></td>
                    <td></td>
                </tr>
        """
        def format_size(size):
            """格式化文件大小"""
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} PB"
        
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            size_str = "-"
            mtime_str = "-"
            file_type = "📄"
            
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                file_type = "📁"
            else:
                # 获取文件大小
                try:
                    size = os.path.getsize(fullname)
                    size_str = format_size(size)
                except OSError:
                    size_str = "-"
                # 获取修改时间
                try:
                    mtime = os.path.getmtime(fullname)
                    mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                except OSError:
                    mtime_str = "-"
            html += f"""
                <tr>
                    <td><span class="{'dir-icon' if os.path.isdir(fullname) else 'file-icon'}">{file_type}</span></td>
                    <td><a href="{urllib.parse.quote(linkname)}">{displayname}</a></td>
                    <td class="size">{size_str}</td>
                    <td class="time">{mtime_str}</td>
                </tr>
            """
        html += f"""
            </table>
            <div class="footer">
                <p>📡 高速文件服务器 | 支持断点续传 | 优化下载速度</p>
            </div>
        </body>
        </html>
        """
        encoded = html.encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(encoded)
        return None
    
    def log_message(self, format, *args):
        pass
    
    def copyfile(self, source, outputfile):
        """优化文件传输，使用更大的缓冲区"""
        try:
            while True:
                buf = source.read(self.buffer_size)
                if not buf:
                    break
                outputfile.write(buf)
                outputfile.flush()
        except Exception as e:
            logger.error(f"文件传输错误: {e}")
            raise

def run_server(port, directory):
    global server_info
    try:
        server_info['running'] = True
        server_info['error'] = None
        ip = '0.0.0.0'
        
        logger.info(f"准备启动HTTP服务器...")
        logger.info(f"服务目录: {directory}")
        logger.info(f"绑定地址: {ip}:{port}")
        
        if not os.path.exists(directory):
            logger.error(f"错误: 目录不存在: {directory}")
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"已创建目录: {directory}")
            except Exception as e:
                logger.error(f"无法创建目录: {e}")
                server_info['error'] = f"无法访问目录: {directory}\n错误: {str(e)}"
                server_info['running'] = False
                return
        
        try:
            test_file = os.path.join(directory, '.test_permission')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            logger.info(f"目录权限检查通过: {directory}")
        except Exception as e:
            logger.error(f"目录权限检查失败: {e}")
            server_info['error'] = f"目录权限不足: {directory}\n错误: {str(e)}"
            server_info['running'] = False
            return
        
        try:
            os.chdir(directory)
            logger.info(f"当前工作目录: {os.getcwd()}")
            try:
                files = os.listdir('.')
                logger.info(f"目录内容: {files[:10]}")
            except Exception as e:
                logger.error(f"无法列出目录内容: {e}")
        except Exception as e:
            logger.error(f"无法切换目录: {e}")
            server_info['error'] = f"无法切换到目录: {directory}\n错误: {str(e)}"
            server_info['running'] = False
            return
        
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind((ip, port))
            test_socket.close()
            logger.info(f"端口 {port} 可用")
        except Exception as e:
            logger.error(f"端口绑定失败: {e}")
            server_info['error'] = f"无法绑定端口 {port}\n错误: {str(e)}"
            server_info['running'] = False
            return
        
        Handler = CustomHTTPRequestHandler
        
        # 使用ThreadingTCPServer支持多线程并发处理请求
        server_info['httpd'] = socketserver.ThreadingTCPServer((ip, port), Handler)
        # 允许地址重用，避免端口占用问题
        server_info['httpd'].allow_reuse_address = True
        
        logger.info(f"HTTP服务器已启动: http://{ip}:{port}")
        logger.info(f"服务目录: {os.getcwd()}")
        logger.info(f"本地访问地址: http://127.0.0.1:{port}")
        
        local_ip = get_local_ip()
        logger.info(f"局域网访问地址: http://{local_ip}:{port}")
        
        server_info['httpd'].serve_forever()
        
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        server_info['error'] = str(e)
        server_info['running'] = False
        server_info['httpd'] = None

def stop_server():
    global server_info
    try:
        logger.info("开始停止服务器...")
        
        if server_info['httpd']:
            logger.info("正在停止服务器进程...")
            try:
                server_info['httpd'].shutdown()
                logger.info("服务器shutdown调用成功")
            except Exception as e:
                logger.error(f"shutdown调用失败: {e}")
            
            time.sleep(1)
            
            try:
                server_info['httpd'].server_close()
                logger.info("服务器server_close调用成功")
            except Exception as e:
                logger.error(f"server_close调用失败: {e}")
            
            server_info['httpd'] = None
        
        server_info['running'] = False
        server_info['error'] = None
        server_info['thread'] = None
        
        logger.info("服务器已完全停止")
    except Exception as e:
        logger.error(f"停止服务器时出错: {e}")
        server_info['running'] = False
        server_info['httpd'] = None
        server_info['thread'] = None

# Kivy配置必须在导入其他Kivy模块之前
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'exit_on_escape', '1')

# 导入字体相关模块
from kivy.core.text import LabelBase
from kivy.utils import platform

# 全局字体变量
chinese_font = 'Roboto'

def setup_fonts():
    """设置中文字体"""
    global chinese_font
    try:
        if platform == 'android':
            font_candidates = [
                '/system/fonts/NotoSansCJK-Regular.ttc',
                '/system/fonts/NotoSansSC-Regular.ttc',
                '/system/fonts/NotoSansCJK-Medium.ttc',
            ]
            for font_path in font_candidates:
                if os.path.exists(font_path):
                    LabelBase.register('ChineseFont', font_path)
                    chinese_font = 'ChineseFont'
                    break
        elif platform == 'win':
            font_candidates = [
                'C:\\Windows\\Fonts\\msyh.ttc',
                'C:\\Windows\\Fonts\\simhei.ttf',
                'C:\\Windows\\Fonts\\simsun.ttc',
                'C:\\Windows\\Fonts\\msyhbd.ttc',
            ]
            for font_path in font_candidates:
                if os.path.exists(font_path):
                    LabelBase.register('ChineseFont', font_path)
                    chinese_font = 'ChineseFont'
                    break
    except Exception as e:
        logger.error(f'Font setup error: {e}')
        pass

# 初始化字体
setup_fonts()


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

# 版本信息
APP_VERSION = "3.0"
BUILD_DATE = "2026-03-18"

# 字体大小设置 (调整为60%)
TITLE_FONT_SIZE = 48
PORT_LABEL_FONT_SIZE = 29
PORT_INPUT_FONT_SIZE = 29
STATUS_FONT_SIZE = 26
BUTTON_FONT_SIZE = 34
VERSION_FONT_SIZE = 18
PADDING = 24
SPACING = 18

class FileServerApp(App):
    def __init__(self, **kwargs):
        super(FileServerApp, self).__init__(**kwargs)
        self.server_thread = None
        self.server_running = False
        self.current_port = 8000
    
    def build(self):
        logger.info("开始构建应用界面")
        
        # 创建布局
        layout = BoxLayout(orientation='vertical', padding=PADDING, spacing=SPACING)
        
        # 创建标题标签 - 使用中文字体
        title = Label(
            text='文件服务器', 
            font_size='48sp', 
            halign='center', 
            size_hint=(1, 0.18),
            valign='middle',
            color=(0.2, 0.6, 1, 1),
            font_name=chinese_font
        )
        layout.add_widget(title)
        
        # 创建端口输入区域
        port_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, 0.12))
        
        # 左侧占位符
        port_layout.add_widget(Widget(size_hint_x=1))
        
        port_label = Label(
            text='端口：', 
            font_size='29sp',
            valign='middle',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_x=None,
            width=100,
            font_name=chinese_font
        )
        
        self.port_input = TextInput(
            text=str(self.current_port), 
            font_size='22sp', 
            multiline=False,
            input_filter='int',
            size_hint=(None, 1),
            width=150,
            padding=16,
            halign='center',
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.4, 0.7, 1, 1),
            font_name=chinese_font
        )
        
        port_layout.add_widget(port_label)
        port_layout.add_widget(self.port_input)
        
        # 右侧占位符
        port_layout.add_widget(Widget(size_hint_x=1))
        
        layout.add_widget(port_layout)
        
        # 创建目录选择区域
        dir_container = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        
        # 目录标签
        dir_label = Label(
            text='目录：', 
            font_size='29sp',
            halign='center',
            size_hint=(1, 0.4),
            valign='middle',
            color=(0.9, 0.9, 0.9, 1),
            font_name=chinese_font
        )
        dir_container.add_widget(dir_label)
        
        # 目录选择器
        dir_spinner_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))
        
        # 左侧占位符
        dir_spinner_layout.add_widget(Widget(size_hint_x=1))
        
        # 检测可用目录
        available_dirs = detect_available_directories()
        if not available_dirs:
            available_dirs = [APP_DIR]
        
        # 创建目录选择器
        self.dir_spinner = Spinner(
            text=available_dirs[0],
            values=available_dirs,
            size_hint_x=None,
            width=400,
            font_size='29sp',
            background_color=(0.2, 0.2, 0.3, 1),
            color=(1, 1, 1, 1),
            font_name=chinese_font
        )
        
        dir_spinner_layout.add_widget(self.dir_spinner)
        
        # 右侧占位符
        dir_spinner_layout.add_widget(Widget(size_hint_x=1))
        
        dir_container.add_widget(dir_spinner_layout)
        
        layout.add_widget(dir_container)
        
        # 创建状态标签
        self.status_label = Label(
            text='点击开始按钮启动服务', 
            font_size='26sp', 
            halign='center',
            size_hint=(1, 0.25),
            valign='middle',
            color=(0.8, 0.8, 0.8, 1),
            font_name=chinese_font
        )
        layout.add_widget(self.status_label)
        
        # 创建启动按钮
        self.start_button = Button(
            text='启动服务', 
            size_hint=(1, 0.18), 
            font_size='34sp',
            padding=30,
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_name=chinese_font
        )
        self.start_button.bind(on_press=self.toggle_server)
        layout.add_widget(self.start_button)
        
        # 创建版本信息标签
        version_label = Label(
            text=f'v{APP_VERSION} ({BUILD_DATE})',
            font_size=VERSION_FONT_SIZE,
            halign='center',
            size_hint=(1, 0.07),
            valign='middle',
            color=(0.5, 0.5, 0.5, 1),
            font_name=chinese_font
        )
        layout.add_widget(version_label)
        
        logger.info("应用界面构建完成")
        return layout
    
    def toggle_server(self, instance):
        if not self.server_running:
            try:
                port = int(self.port_input.text)
                if port < 1 or port > 65535:
                    self.status_label.text = '端口必须在1-65535之间'
                    self.status_label.color = (1, 0.5, 0.5, 1)
                    return
            except ValueError:
                self.status_label.text = '请输入有效的端口号'
                self.status_label.color = (1, 0.5, 0.5, 1)
                return
            
            if not is_port_available(port):
                available_port = get_available_port(port)
                if available_port:
                    self.port_input.text = str(available_port)
                    port = available_port
                    self.status_label.text = f'端口 {port} 已被占用，已切换到 {available_port}'
                    self.status_label.color = (1, 1, 0.5, 1)
                else:
                    self.status_label.text = '未找到可用端口'
                    self.status_label.color = (1, 0.5, 0.5, 1)
                    return
            
            self.current_port = port
            
            self.start_button.text = '启动中...'
            self.start_button.disabled = True
            self.start_button.background_color = (0.2, 0.5, 0.8, 1)
            self.status_label.text = f'正在启动服务器...\n端口: {port}'
            self.status_label.color = (0.8, 0.8, 0.8, 1)
            
            def delayed_start(dt):
                if server_info['running']:
                    stop_server()
                    time.sleep(1)
                
                # 再次检查权限，确保用户已授予
                if not check_android_permissions():
                    self.server_running = False
                    self.start_button.text = '启动服务'
                    self.start_button.disabled = False
                    self.start_button.background_color = (0.3, 0.6, 0.9, 1)
                    self.status_label.text = '权限不足，请授予存储权限后重试'
                    self.status_label.color = (1, 0.5, 0.5, 1)
                    logger.warning("Permission check failed")
                    return
                
                selected_dir = self.dir_spinner.text
                server_info['thread'] = threading.Thread(target=run_server, args=(port, selected_dir), daemon=True)
                server_info['thread'].start()
                
                def check_server_status(dt):
                    if server_info['error']:
                        self.server_running = False
                        self.start_button.text = '启动服务'
                        self.start_button.disabled = False
                        self.start_button.background_color = (0.3, 0.6, 0.9, 1)
                        self.status_label.text = f'启动失败: {server_info["error"]}'
                        self.status_label.color = (1, 0.5, 0.5, 1)
                        logger.error(f"Server start failed: {server_info['error']}")
                    elif server_info['running']:
                        self.server_running = True
                        self.start_button.text = '停止服务'
                        self.start_button.disabled = False
                        self.start_button.background_color = (0.8, 0.4, 0.4, 1)
                        local_ip = get_local_ip()
                        selected_dir = self.dir_spinner.text
                        self.status_label.text = f'服务已启动\n访问地址: http://{local_ip}:{port}\n根目录: {selected_dir}'
                        self.status_label.color = (0.5, 1, 0.5, 1)
                        logger.info(f"Server started: http://{local_ip}:{port} with directory: {selected_dir}")
                    else:
                        Clock.schedule_once(check_server_status, 0.5)
                
                Clock.schedule_once(check_server_status, 1.0)
            
            Clock.schedule_once(delayed_start, 0.1)
        else:
            self.start_button.text = '停止中...'
            self.start_button.disabled = True
            self.start_button.background_color = (0.2, 0.5, 0.8, 1)
            self.status_label.text = '正在停止服务器...'
            self.status_label.color = (0.8, 0.8, 0.8, 1)
            
            def delayed_stop(dt):
                stop_server()
                time.sleep(2)
                self.server_running = False
                self.start_button.text = '启动服务'
                self.start_button.disabled = False
                self.start_button.background_color = (0.3, 0.6, 0.9, 1)
                self.status_label.text = '服务已停止\n点击启动按钮开始'
                self.status_label.color = (0.8, 0.8, 0.8, 1)
                logger.info("Server stopped")
            
            Clock.schedule_once(delayed_stop, 0.1)

if __name__ == '__main__':
    try:
        logger.info("Application starting")
        # 检查Android权限
        check_android_permissions()
        app = FileServerApp()
        app.run()
    except Exception as e:
        logger.error(f"Application failed: {e}")
        port = get_available_port()
        if port:
            run_server(port)
        else:
            logger.error("No available port")
        sys.exit(0)
