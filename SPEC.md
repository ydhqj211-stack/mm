# SMS Watcher - 远程短信监控应用

## 1. 项目概述

**项目名称:** SMS Watcher
**项目类型:** Android 移动应用 (Python + Kivy)
**核心功能:** 监控安卓手机短信并通过Telegram Bot实时推送到远程设备
**目标用户:** 需要远程监控自己手机短信的用户

## 2. 技术方案

### 框架选择
- **GUI框架:** Kivy (跨平台Python框架)
- **短信访问:** Android BroadcastReceiver (通过plyer库)
- **消息推送:** python-telegram-bot (Telegram Bot API)
- **打包工具:** Buildozer (将Python应用打包为APK)

### 核心功能
1. **短信监控** - 实时监听新收到的短信
2. **历史短信** - 读取手机中已有的短信
3. **Telegram推送** - 将短信内容通过Bot发送到指定Chat
4. **Web管理界面** - 本地Web界面查看和管理

## 3. 功能列表

### 核心功能
- [ ] 实时监控新收到的短信
- [ ] 读取手机历史短信
- [ ] Telegram Bot消息推送
- [ ] 应用后台运行
- [ ] 开机自启动
- [ ] 简洁的图形界面

### 配置功能
- [ ] Telegram Bot Token设置
- [ ] Telegram Chat ID设置
- [ ] 监控开关控制
- [ ] 推送过滤规则（可选）

## 4. 界面设计

### 主界面
- 状态显示（连接状态、监控状态）
- 最近短信列表（显示最近10条）
- Telegram配置入口
- 开始/停止监控按钮

### 配置界面
- Telegram Bot Token输入框
- Telegram Chat ID输入框
- 测试连接按钮

## 5. 数据流向

```
[手机收到短信]
    ↓
[SMS Watcher App 监听]
    ↓
[格式化短信内容]
    ↓
[Telegram Bot API]
    ↓
[用户Telegram收到通知]
```

## 6. 安全考虑

- Token和配置信息本地加密存储
- 仅监控，不进行任何远程控制
- 用户数据仅保存在本地设备

## 7. 依赖库

```
kivy>=2.1.0
plyer>=2.0.0
python-telegram-bot>=13.0
android.runnable>=0.1.0
```

## 8. 运行环境

- Android 5.0+ (API 21+)
- Python 3.8+
- 需要授予短信权限