# Arknights-Recruit-Tool

明日方舟公开招募计算器 for iOS

## 首页

[明日方舟公开招募计算器](https://akhr.imwtx.com)

## 开发

### 环境依赖

- Python 3.11+
- Tesseract OCR
- `ark_recruit.traineddata` 放在项目根目录

### 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

### 本地启动

```bash
python3 app.py
```

### 运行测试

```bash
python3 -m pytest
```

## 安装

在 iPhone/iPad Safari 浏览器中打开链接获取快捷指令，滑至底部点击添加。如果没有安装「快捷指令」App，先到 App Store 下载安装。

如果提示快捷指令不受信任无法打开，前往 设置 - 快捷指令 - 允许不受信任的快捷指令。

如果以上选项为灰色无法开启，打开快捷指令任意添加一个并运行一次即可。

## 使用

两种推荐的使用方法：

1. 设置 - 辅助功能 - 触控 - 辅助触控 - 开启辅助触控功能(也就是小白点)；然后自定顶层菜单 - 新增一个图标 - 选择快捷指令中的「公开招募」；现在只需要打开游戏，然后点击小白点中的「公开招募」，就可以获得计算结果。

2. 设置 - 辅助功能 - 触控 - 轻点背面 - 轻点两下 - 选择快捷指令中的「公开招募」；然后在游戏内的公招页面轻敲两下手机背面即可。

**注意**：调用脚本时公开招募页面不要选择任何 tag，否则可能会影响识别结果。

## 数据更新

项目现在可以通过 GitHub Actions 自动同步公开招募数据源到 `data/recruitment.json`。

手动更新也可以直接运行：

```bash
python3 scripts/update_recruit_data.py
```

默认数据源为 MAA 的 `dev-v2` 分支 `resource/recruitment.json`。
