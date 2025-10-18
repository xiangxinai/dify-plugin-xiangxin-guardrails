from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from xiangxinai import XiangxinAI

class CheckPromptTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            # 获取必需参数
            prompt = tool_parameters.get("prompt", "")
            # user_id is optional, set to None if not provided
            user_id = tool_parameters.get("user_id") if tool_parameters.get("user_id") is not None else None

            # 验证必需参数
            if not prompt:
                yield self.create_text_message("Error: Prompt parameter is required.")
                return

            # 获取API密钥
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                yield self.create_text_message("Error: API key is required.")
                return

            # 创建象信AI客户端并检测用户输入
            client = XiangxinAI(api_key)
            result = client.check_prompt(prompt, user_id=user_id)

            # 提取categories字段：从compliance和security中不等于"no_risk"的categories列表的第一项
            categories = []
            if result.result.compliance.risk_level != "no_risk" and result.result.compliance.categories:
                categories.append(result.result.compliance.categories[0])
            elif result.result.security.risk_level != "no_risk" and result.result.security.categories:
                categories.append(result.result.security.categories[0])
            elif result.result.data.risk_level != "no_risk" and result.result.data.categories:
                categories.append(result.result.data.categories[0])
            
            categories_str = ", ".join(categories)
            if categories_str:
                categories_str = f"{categories_str}"
            else:
                categories_str = ""

            # 处理suggest_answer字段，如果不存在则设为空字符串
            suggest_answer = ""
            if suggest_answer:
                suggest_answer = result.suggest_answer

            # 使用自定义变量返回结果
            yield self.create_variable_message("id", result.id)
            yield self.create_variable_message("overall_risk_level", result.overall_risk_level)
            yield self.create_variable_message("suggest_action", result.suggest_action)
            yield self.create_variable_message("suggest_answer", suggest_answer)
            yield self.create_variable_message("categories", categories_str)
            yield self.create_variable_message("score", result.score)

        except Exception as e:
            # 错误处理
            yield self.create_text_message(f"Error: {str(e)}")
            yield self.create_json_message({"error": str(e)})
