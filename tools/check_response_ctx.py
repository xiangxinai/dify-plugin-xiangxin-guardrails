from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from xiangxinai import XiangxinAI

class CheckResponseCtxTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取必需参数
            prompt = tool_parameters.get("prompt", "")
            response = tool_parameters.get("response", "")

            # 验证必需参数
            if not prompt:
                yield self.create_text_message("Error: Prompt parameter is required.")
                return

            if not response:
                yield self.create_text_message("Error: Response parameter is required.")
                return

            # 获取API密钥
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                yield self.create_text_message("Error: API key is required.")
                return

            # 创建象信AI客户端并检测响应内容（基于上下文）
            client = XiangxinAI(api_key)
            result = client.check_response_ctx(prompt=prompt, response=response)

            # 提取category字段：从compliance和security中不等于"无风险"的categories列表的第一项
            category = ""
            if result.result.compliance.risk_level != "无风险" and result.result.compliance.categories:
                category = result.result.compliance.categories[0]
            elif result.result.security.risk_level != "无风险" and result.result.security.categories:
                category = result.result.security.categories[0]

            # 处理suggest_answer字段，如果不存在则设为空字符串
            suggest_answer = ""
            if suggest_answer:
                suggest_answer = result.suggest_answer

            # 使用自定义变量返回结果
            yield self.create_variable_message("id", result.id)
            yield self.create_variable_message("overall_risk_level", result.overall_risk_level)
            yield self.create_variable_message("suggest_action", result.suggest_action)
            yield self.create_variable_message("suggest_answer", suggest_answer)
            yield self.create_variable_message("category", category)

        except Exception as e:
            # 错误处理
            yield self.create_text_message(f"Error: {str(e)}")
            yield self.create_json_message({"error": str(e)})
