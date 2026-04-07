# Changelog

## 2026-04-08

### Refactor

- 将项目重构为分层的 Flask 单体应用，主代码迁移到 `ark_recruit_tool/`
- 保留 `POST /` 的旧 JSON 响应形态，继续兼容 iOS 快捷指令
- 将 OCR、图像处理、招募分析、文本渲染和数据访问解耦
- 为运行时异常增加 JSON 兜底，避免快捷指令收到 HTML 500 页面

### Data

- 将公开招募数据从 `data/operators.py` 和 `data/top_operators.py` 迁移到 `data/recruitment.json`
- 更新数据同步脚本，统一输出单个 JSON 文件
- 为数据文件增加 `source`、`generated_at`、`operator_count` 元数据
- 在仓储层增加基础 schema 校验

### Web

- 重做首页和捐赠页的模板与样式，移除对 Bootstrap-Flask 的依赖
- 保留原有页面用途，不新增额外的网页上传识别入口

### Testing

- 新增 `pytest` 测试集，覆盖 tag 归一化、组合分析、文本渲染、仓储校验、路由和服务编排

### Security

- 升级关键依赖到安全版本：
  - `Flask 3.1.3`
  - `Werkzeug 3.1.6`
  - `Pillow 12.1.1`
- 清理 GitHub Dependabot 安全告警
