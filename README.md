### README 文件

#### 简介
这是一个用于在区块链网络上执行自动交易的Python脚本。脚本通过Web3与区块链网络交互，执行循环交易。

#### 配置步骤

1. **安装依赖**: 确保安装了`web3`包。如果没有安装，可以通过运行`pip install web3`来安装。

2. **配置文件**: 修改`config.json`文件，按照以下说明配置每个字段：
   - `private_keys`: 您的钱包私钥数组。例如：`["私钥1", "私钥2"]`。
   - `inscription_text`: 交易中包含的文本信息。
   - `self_transfer_address`: 自转账的地址。如果不进行自转账，则留空。
   - `interval_milliseconds`: 两次交易之间的等待时间，单位为毫秒。
   - `rpc_url`: 用于连接到区块链网络的RPC URL。
   - `gas`: 交易的gas限制。
   - `max_gas`: 最大gas价格限制。如果设置为`true`，将使用网络当前的最大gas价格。

3. **运行脚本**: 通过命令`python main.py`运行脚本。在提示时输入循环次数。

#### 注意事项
- 保证`config.json`文件中的配置正确无误。
- 确保你的钱包有足够的余额来支付gas费用。
- 使用私钥时需谨慎，避免泄露。

#### 安全提示
不要公开您的私钥，以防止资金损失。始终在安全的环境下操作。