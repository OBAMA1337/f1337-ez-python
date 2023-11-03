from web3 import Web3
import time

# Replace link with your alchemy url
alchemy_url = "https://base-mainnet.g.alchemy.com/v2/000000000000"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Replace 0x000000000 with your account's private key
private_key = "0x000000000"

contract_address = "0x15EBaAD8717A6B71116ffAF1E0FD4A3b4DE0F96C"

# Specify the function signature for the "mint" function
function_signature = "0x1249c58b"

# Define your target lottery number
target_lottery_number = 1337

sleep_time = 0.3

while True:
    # Get the block information for the latest block
    latest_block = w3.eth.get_block("latest")

    # Get the block hash as a binary format
    block_hash = latest_block["hash"]

    # Calculate the lottery number based on the block hash
    lottery_number = int(block_hash.hex(), 16) % 10000

    print(f"Latest block number: {latest_block['number']}, Lottery number: {lottery_number}")

    if lottery_number == target_lottery_number:
        # Input your address here instead of "0x00000000"
        your_ethereum_address = "0x00000000"
        to_address = w3.to_checksum_address(your_ethereum_address)
        nonce = w3.eth.get_transaction_count(to_address)

        gas_price = w3.to_wei("1", "gwei")  # Adjust the gas price as needed
        gas_limit = 80000  # Adjust the gas limit as needed

        # Calculate the chain ID
        chain_id = w3.eth.chain_id

        # Create the transaction
        transaction = {
            "to": contract_address,
            "value": 0,
            "gas": gas_limit,
            "gasPrice": gas_price,
            "nonce": nonce,
            "data": function_signature,
            "chainId": chain_id  # Add the chain ID to the transaction
        }

        # Sign the transaction
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

        # Send the signed transaction
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        print(f"Sent transaction to mint token. Transaction hash: {tx_hash.hex()}")

        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(tx_hash)

    # Wait for the next check
    time.sleep(sleep_time)
