#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.utils import platform
from flask import Flask, send_from_directory, render_template_string, request
from werkzeug.utils import secure_filename

try:
    from android.permissions import request_permissions, Permission
    from android.storage import app_storage_path, primary_external_storage_path
except ImportError:
    pass

class HTTPServerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_thread = None
        self.server = None
        self.is_running = False
        self.host = '0.0.0.0'
        self.port = 8000
        self.base_dir = None
        self.chinese_font = None

    def build(self):
        self.setup_fonts()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title_label = Label(text='手机HTTP文件服务器', font_size=24, size_hint_y=None, height=50, font_name=self.chinese_font)
        layout.add_widget(title_label)
        
        self.ip_label = Label(text='IP地址: 检测中...', font_size=16, size_hint_y=None, height=40, font_name=self.chinese_font)
        layout.add_widget(self.ip_label)
        
        self.port_input = TextInput(text=str(self.port), hint_text='端口', font_size=16, size_hint_y=None, height=40, font_name=self.chinese_font)
        layout.add_widget(self.port_input)
        
        self.path_input = TextInput(text='/', hint_text='访问目录', font_size=16, size_hint_y=None, height=40, font_name=self.chinese_font)
        layout.add_widget(self.path_input)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.start_button = Button(text='启动服务器', font_size=16, font_name=self.chinese_font)
        self.start_button.bind(on_press=self.toggle_server)
        button_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='停止服务器', font_size=16, disabled=True, font_name=self.chinese_font)
        self.stop_button.bind(on_press=self.toggle_server)
        button_layout.add_widget(self.stop_button)
        layout.add_widget(button_layout)
        
        self.status_label = Label(text='状态: 服务器未启动', font_size=16, size_hint_y=None, height=40, font_name=self.chinese_font)
        layout.add_widget(self.status_label)
        
        self.log_view = ScrollView(size_hint_y=1)
        self.log_text = Label(text='', font_size=12, size_hint_y=None, markup=True, font_name=self.chinese_font)
        self.log_text.bind(texture_size=self.update_log_height)
        self.log_view.add_widget(self.log_text)
        layout.add_widget(self.log_view)
        
        self.update_ip()
        self.setup_base_dir()
        return layout
    
    def setup_fonts(self):
        self.chinese_font = 'Roboto'
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
                        self.chinese_font = 'ChineseFont'
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
                        self.chinese_font = 'ChineseFont'
                        break
        except Exception as e:
            print(f'Font setup error: {e}')
            pass
    
    def setup_base_dir(self):
        if platform == 'android':
            try:
                self.base_dir = primary_external_storage_path()
            except:
                try:
                    self.base_dir = app_storage_path()
                except:
                    self.base_dir = '/sdcard'
        else:
            self.base_dir = os.path.expanduser('~')
        self.path_input.text = self.base_dir
    
    def update_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            self.ip_label.text = f'IP地址: {ip}'
        except:
            self.ip_label.text = 'IP地址: 无法获取'
    
    def update_log_height(self, instance, value):
        instance.height = instance.texture_size[1]
    
    def log(self, message):
        self.log_text.text += f'[color=000000]{message}[/color]\n'
    
    def toggle_server(self, instance):
        if self.is_running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        try:
            self.port = int(self.port_input.text)
            self.base_dir = self.path_input.text
            
            if platform == 'android':
                try:
                    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.INTERNET])
                except:
                    pass
            
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
            
            self.is_running = True
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.status_label.text = '状态: 服务器运行中'
            self.log(f'服务器已启动，访问地址: http://{self.ip_label.text.replace("IP地址: ", "")}:{self.port}')
            
        except Exception as e:
            self.log(f'启动失败: {str(e)}')
    
    def stop_server(self):
        self.is_running = False
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.status_label.text = '状态: 服务器未启动'
        self.log('服务器已停止')
    
    def run_server(self):
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            path = request.args.get('path', '/')
            full_path = os.path.join(self.base_dir, path.lstrip('/'))
            
            if not os.path.exists(full_path):
                return '路径不存在', 404
            
            if os.path.isfile(full_path):
                return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), as_attachment=True)
            
            items = []
            for item in sorted(os.listdir(full_path)):
                item_path = os.path.join(full_path, item)
                item_type = 'dir' if os.path.isdir(item_path) else 'file'
                items.append({'name': item, 'type': item_type, 'path': os.path.join(path, item).replace('\\', '/')})
            
            parent_path = os.path.dirname(path) if path != '/' else '/'
            
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>文件服务器</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .path { background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                    th { background: #4CAF50; color: white; }
                    tr:hover { background: #f5f5f5; }
                    a { color: #2196F3; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <h1>📁 文件服务器</h1>
                <div class="path">当前路径: {{ current_path }}</div>
                {% if parent_path != current_path %}
                <p><a href="?path={{ parent_path }}">⬆️ 返回上级目录</a></p>
                {% endif %}
                <table>
                    <tr>
                        <th>类型</th>
                        <th>名称</th>
                    </tr>
                    {% for item in items %}
                    <tr>
                        <td>{% if item.type == 'dir' %}📁{% else %}📄{% endif %}</td>
                        <td><a href="?path={{ item.path }}">{{ item.name }}</a></td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
            '''
            
            return render_template_string(html, items=items, current_path=path, parent_path=parent_path)
        
        @app.errorhandler(404)
        def not_found(error):
            return '页面未找到', 404
        
        @app.errorhandler(500)
        def server_error(error):
            return f'服务器错误: {str(error)}', 500
        
        try:
            app.run(host=self.host, port=self.port, debug=False, use_reloader=False, threaded=True)
        except Exception as e:
            self.log(f'服务器错误: {str(e)}')

if __name__ == '__main__':
    HTTPServerApp().run()
