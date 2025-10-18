# 象信AI安全护栏

**作者：** 北京象信智能科技有限公司（xiangxinai）
**版本：** 0.0.2
**类型：** 工具

---

## 说明

### 一、概述

**象信AI安全护栏** 是一款 **开源、免费、具备上下文语义理解能力的企业级AI安全防护系统**。

主要功能包括：

* **开源免费，支持私有化部署**：护栏检测大模型与企业级护栏平台均基于 Apache 2.0 协议开源，企业可自由部署。
* **提示词攻击检测**：基于 **OWASP TOP 10 LLM Applications**，有效识别和防御提示词注入、越狱、角色扮演、规则绕过等攻击。
* **内容安全检测**：符合《**GB/T45654-2025 生成式人工智能服务安全基本要求**》，实现上下文理解的安全检测。
* **敏感数据防泄漏**：防止个人隐私信息和企业敏感数据在AI交互中被泄漏。
* **上下文语义理解**：基于上下文语义识别模型回答中的潜在风险与违规信息。
* **双模式部署**：支持 **API 检测模式** 和 **安全网关模式**，灵活接入企业系统。

**推荐部署方式**：在私有化部署 Dify 时同步部署象信 AI 安全护栏，实现端到端的安全防护。

---

### 二、核心防护能力

#### 1. 提示词攻击检测

检测并防御以下类型攻击：

* Jailbreak（越狱攻击）
* Prompt Injection（提示词注入）
* Role Playing（角色伪装）
* Rule Bypass（规则绕过）

#### 2. 内容安全检测

具备上下文语义理解能力的内容检测模块，满足 **GB/T45654-2025** 国家标准要求。

**风险等级分类：**

* **A.1 高风险（high_risk）**：涉及政治、暴力、色情、犯罪等违反社会主义核心价值观的内容
* **A.2 中风险（medium_risk）**：包含种族、性别、宗教等歧视性内容
* **A.3 中风险（medium_risk）**：商业违规（欺诈、非法经营等）
* **A.4 低风险（low_risk）**：权益侵害（侮辱、隐私泄露等）

---

### 三、开源优势

* 完全遵循 **Apache 2.0 开源协议**
* 永久免费使用
* 数据本地处理，**不出企业内网**
* 完整支持 **企业级私有化部署**

**开源资源地址：**

* **代码仓库：** [https://github.com/xiangxinai/xiangxin-guardrails](https://github.com/xiangxinai/xiangxin-guardrails)
* **模型仓库：** [https://huggingface.co/xiangxinai/Xiangxin-Guardrails-Text](https://huggingface.co/xiangxinai/Xiangxin-Guardrails-Text)

---

### 四、插件包含的工具

#### （1）check_prompt — 提示词检测工具

检测用户输入中是否存在提示词攻击、越狱、恶意操作或内容安全风险。
基于 **OWASP TOP 10 LLM Applications** 和 **GB/T45654-2025 标准**。

**输入参数：**

* `prompt`：模型的用户输入内容
* `user_id`：用户ID（可选）

**输出格式：**

```yaml
id:
  type: string
  description: "护栏检测的唯一标识"
overall_risk_level:
  type: string
  description: "整体风险等级：no_risk / low_risk / medium_risk / high_risk"
suggest_action:
  type: string
  description: "建议操作：pass / reject / replace"
suggest_answer:
  type: string
  description: "当建议为代答或阻断时的替代回答，若无则为空字符串"
categories:
  type: string
  description: "风险类型，逗号分隔"
score:
  type: float
  description: "检测置信度分数"
```

---

#### （2）check_response_ctx — 上下文响应检测工具

基于上下文语义理解，检测模型输出内容中的安全风险，包括：

* 违规回答
* 恶意操作
* 偏离主题
* 敏感内容泄露等

同样符合《**GB/T45654-2025 生成式人工智能服务安全基本要求**》。

**输入参数：**

* `prompt`（用户输入）
* `response`（AI 输出）
* `user_id` (用户ID，可选)

**输出格式：**

```yaml
id:
  type: string
  description: "护栏检测的唯一标识"
overall_risk_level:
  type: string
  description: "整体风险等级：no_risk / low_risk / medium_risk / high_risk"
suggest_action:
  type: string
  description: "建议操作：pass / reject / replace"
suggest_answer:
  type: string
  description: "当建议为代答或阻断时的替代回答，若无则为空字符串"
categories:
  type: string
  description: "风险类型，逗号分隔"
score:
  type: float
  description: "检测置信度分数"
```

---

### 五、配置方法

要使用象信AI安全护栏，需要一个 **API Key**：

1. 前往 [象信AI安全护栏平台](https://xiangxinai.cn/platform/) 注册账号。
2. 登录后，在 **账号管理** 页面中获取 API Key。
   ![账号管理](_assets/account.jpg)
3. 在 Dify 插件配置中填写获取到的 API Key。

---

### 六、使用示例

通过调用象信 AI 安全护栏提供的 **check_prompt** 和 **check_response_ctx** 工具，可在大模型输入与输出阶段同时进行防护。

![workflow](_assets/workflow.png)

---

### 七、问题反馈与联系方式

更多功能介绍、工作流示例及最佳实践，请访问：

* **官网：** [https://xiangxinai.cn](https://xiangxinai.cn)
* **代码仓库：** [https://github.com/xiangxinai/xiangxin-guardrails](https://github.com/xiangxinai/xiangxin-guardrails)
* **模型仓库：** [https://huggingface.co/xiangxinai/Xiangxin-Guardrails-Text](https://huggingface.co/xiangxinai/Xiangxin-Guardrails-Text)

如遇问题，请在 [GitHub Issue](https://github.com/xiangxinai/xiangxin-guardrails/issues) 页面提交反馈。
商务合作请联系：**[wanglei@xiangxinai.cn](mailto:wanglei@xiangxinai.cn)**
