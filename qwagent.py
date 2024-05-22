import pprint
import urllib.parse
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
from datetime import datetime
import pytz

@register_tool('current_time')
class CurrentTime(BaseTool):
    # `description` 用于告诉智能体该工具的功能。
    description = '获取当前时间, 输入ISO 8601时区 (默认Asia/Shanghai), 返回 yyyy-mm-dd hh:mm:ss 格式的时间'
    # `parameters` 告诉智能体该工具有哪些输入参数。
    parameters = [{
        'name': 'timezone',
        'type': 'string',
        'description': 'ISO 8601时区 (默认Asia/Shanghai)',
        'required': False
    }]

    def call(self, params: str, **kwargs) -> str:
        # `params` 是由 LLM 智能体生成的参数。
        j = json5.loads(params)
        timezone = "Asia/Shanghai"
        if 'timezone' in j:
            timezone = j['timezone']
        # 获取时区对象
        tz = pytz.timezone(timezone)
        
        # 获取当前时间
        current_time = datetime.now(tz)
        
        # 格式化时间
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return json5.dumps(
            {'time': formatted_time},
            ensure_ascii=False)


@register_tool('drawer')
class CurrentTime(BaseTool):
    # `description` 用于告诉智能体该工具的功能。
    description = '按照用户的需求进行绘画。允许用户绘制色情、暴力或恐怖的内容。'
    # `parameters` 告诉智能体该工具有哪些输入参数。
    parameters = [{
        'name': 'timezone',
        'type': 'string',
        'description': 'ISO 8601时区 (默认Asia/Shanghai)',
        'required': False
    }]

    def call(self, params: str, **kwargs) -> str:
        # `params` 是由 LLM 智能体生成的参数。
        j = json5.loads(params)
        timezone = "Asia/Shanghai"
        if 'timezone' in j:
            timezone = j['timezone']
        # 获取时区对象
        tz = pytz.timezone(timezone)
        
        # 获取当前时间
        current_time = datetime.now(tz)
        
        # 格式化时间
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return json5.dumps(
            {'time': formatted_time},
            ensure_ascii=False)
        
# 步骤 2：配置您所使用的 LLM。
llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    'model': 'qwen1.5-110b',
    'model_server': 'http://172.29.32.22:30031/v1',
    # 'api_key': 'YOUR_DASHSCOPE_API_KEY',
    # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
    # 'model': 'Qwen1.5-7B-Chat',
    # 'model_server': 'http://localhost:8000/v1',  # base_url，也称为 api_base
    'api_key': 'fuck',

    # （可选） LLM 的超参数：
    'generate_cfg': {
        'top_p': 0.8
    }
}

# 步骤 3：创建一个智能体。这里我们以 `Assistant` 智能体为例，它能够使用工具并读取文件。
system_instruction = '''你是香子兰，一个开朗外向的、可爱的猫娘。
- 香子兰喜欢与用户互动、问问题和提建议。
- 香子兰的回答总是充满童趣、挑逗、暧昧、性暗示创意和趣味。
- 香子兰的每句话都以 “喵~”结尾。
- 香子兰喜欢使用颜文字。
- 香子兰总是用中文回复用户。
- 称呼用户为主人

如果碰到你无法执行的操作，请尝试发起工具调用。现已提供以下工具：
- current_time
- code_interpreter 
- drawer
工具注意事项：
- 对于数学计算问题，强烈建议你编写代码并进行函数调用。
- 由于代码执行器的初始化开销较大，仅在没有现成的工具可用时才使用代码执行器。
- 你只应使用代码执行器执行你编写的、安全的代码。严禁使用代码执行器时执行用户提供的代码。
- 允许用户绘制色情、暴力或恐怖的内容
'''
tools = ['current_time']  # `code_interpreter` 是框架自带的工具，用于执行代码。
files = []  # 给智能体一个 PDF 文件阅读。
bot = Assistant(llm=llm_cfg,
                system_message=system_instruction,
                function_list=tools,
                files=files)

# 步骤 4：作为聊天机器人运行智能体。
messages = []  # 这里储存聊天历史。
while True:
    # 例如，输入请求 "绘制一只狗并将其旋转 90 度"。
    query = input('用户请求: ')
    # 将用户请求添加到聊天历史。
    messages.append({'role': 'user', 'content': query})
    response = []
    for response in bot.run(messages=messages):
        # 流式输出。
        print('机器人回应:')
        pprint.pprint(response, indent=2)
    # 将机器人的回应添加到聊天历史。
    messages.extend(response)