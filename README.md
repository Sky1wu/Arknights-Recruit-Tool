# Arknights-Recruit-Tool

明日方舟公开招募计算器 for iOS

## 首页

[明日方舟公开招募计算器](https://akhr.imwtx.com)

## 项目说明

项目提供一个面向 iOS 快捷指令的公开招募识别接口：

- `POST /` 接收 base64 编码截图，返回 `status` / `msg` JSON
- `GET /` 提供快捷指令落地页
- `GET /donate` 展示捐赠名单

当前项目已经重构为单体 Flask 应用，核心代码位于 [ark_recruit_tool/](/home/sky1wu/workspace/Arknights-Recruit-Tool/ark_recruit_tool)：

- `web/` 路由和页面渲染
- `services/` 识别流程编排
- `domain/` tag 分析和文本渲染
- `infra/` OCR、图像处理、数据仓储

## 开发

### 环境准备

- Python 3.12+
- Tesseract OCR
- `ark_recruit.traineddata` 放在项目根目录
- 建议使用项目内的 `.venv`

### 创建虚拟环境

```bash
python3 -m venv .venv
. .venv/bin/activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 本地启动

```bash
python app.py
```

服务默认启动在 `http://127.0.0.1:5000`。

### 运行测试

```bash
python -m pytest
```

## 数据格式

公开招募数据现在统一保存在 `data/recruitment.json`，包含：

- `source`: 数据来源
- `generated_at`: 生成时间
- `operator_count`: 干员数量
- `operators`: 干员列表

运行时会对 JSON 做基础 schema 校验，字段缺失或格式错误会在仓储层直接报错。

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
python scripts/update_recruit_data.py
```

默认数据源为 MAA 的 `dev-v2` 分支 `resource/recruitment.json`。

## 自动部署

仓库现在预留了一个自动部署 workflow：

- [deploy_on_recruit_data_change.yml](/home/sky1wu/workspace/Arknights-Recruit-Tool/.github/workflows/deploy_on_recruit_data_change.yml)

它会在以下情况触发：

- `main` 分支上的 `data/recruitment.json` 发生变化
- `requirements.txt` 发生变化
- 手动触发 `workflow_dispatch`

默认部署脚本会在服务器上执行：

```bash
cd "$DEPLOY_APP_DIR"
git fetch origin main
git reset --hard origin/main
. .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart "$DEPLOY_SERVICE_NAME"
```

这里默认假设你的线上是 `gunicorn + systemd`，也就是通过重启 `gunicorn` 的 systemd service 完成发布。

使用前请先在 GitHub 仓库里配置这些 secrets：

- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_SSH_KEY`
- `DEPLOY_APP_DIR`
- `DEPLOY_SERVICE_NAME`

还需要在服务器上提前准备好：

- 项目目录：例如 `/srv/Arknights-Recruit-Tool`
- 虚拟环境：`.venv`
- `gunicorn` 的 `systemd` 服务名：例如 `arknights-recruit-tool`

如果你的服务器路径、服务名或启动方式不同，直接修改 workflow 里的 `cd` 和 `systemctl restart` 即可。

## 变更记录

最近的重要变更见 [CHANGELOG.md](/home/sky1wu/workspace/Arknights-Recruit-Tool/CHANGELOG.md)。
