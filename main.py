import json
import time
from web3 import Web3, HTTPProvider, WebsocketProvider


def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)


def main():
    config = load_config()
    if config['rpc_url'].startswith('http://') or config['rpc_url'].startswith('https://'):
        provider = HTTPProvider(config['rpc_url'], request_kwargs={'timeout': 10})
    elif config['rpc_url'].startswith('ws://') or config['rpc_url'].startswith('wss://'):
        provider = WebsocketProvider(config['rpc_url'])
    else:
        raise ValueError("Unsupported protocol in RPC URL")

    w3 = Web3(provider)

    loop_count = input("请输入循环次数（默认5000）: ")
    loop_count = int(loop_count) if loop_count else 5000

    gas_price = config.get('gas_price', None)
    max_gas_price = config.get('max_gas_price', w3.to_wei('100', 'gwei'))

    if not gas_price:
        gas_price = w3.eth.gas_price
    if gas_price > max_gas_price:
        gas_price = max_gas_price

    for _ in range(loop_count):
        for private_key in config['private_keys']:
            account = w3.eth.account.from_key(private_key)
            address = account.address

            balance = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance, 'ether')
            if balance == 0:
                print(f'钱包 {address} 余额为0，跳过...')
                continue
            else:
                print(f'钱包 {address} 当前余额: {balance_eth} MATIC')

            nonce = w3.eth.get_transaction_count(address, 'pending')
            transaction = {
                'to': config['self_transfer_address'] if config['self_transfer_address'] else address,
                'value': 0,
                'data': w3.to_hex(text=config['inscription_text']),
                'gas': config['gas'],
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': w3.eth.chain_id
            }

            try:
                signed_txn = account.sign_transaction(transaction)
                txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(f'钱包 {address} -> 交易哈希: {txn_hash.hex()}')
                receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=config['timeout'])
                print(f'钱包 {address} -> 交易状态: {receipt.status}, 消耗的Gas: {receipt.gasUsed}')
            except Exception as e:
                error_message = str(e)
                if 'already known' in error_message:
                    print(f'钱包 {address} -> 错误: {error_message}')
                    print('检测到 "already known" 错误, 正在暂停并重新获取 nonce...')
                    time.sleep(5)  # 暂停5秒
                    nonce = w3.eth.get_transaction_count(address, 'pending')  # 重新获取 nonce
                    continue  # 可以选择重试或跳过此次循环
                else:
                    if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict) and 'message' in e.args[
                        0]:
                        error_message = e.args[0]['message']
                    print(f'钱包 {address} -> 错误: {error_message}')
            time.sleep(config['interval_milliseconds'] / 1000)  # 增加交易间隔


if __name__ == '__main__':
    main()
