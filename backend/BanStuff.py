from bananopie import RPC, Wallet

rpc = RPC("https://kaliumapi.appditto.com/api")
MAIN_DEPOSIT_WALLET = Wallet(rpc, open("BANWALLET.env", "r").read(), 3)


def new_deposit_keypair() -> dict:
    account = Wallet(rpc)
    return {"seed": account.seed, "address": account.get_address()}


def process_deposit(keypair: dict) -> float:
    account = Wallet(rpc, keypair["seed"])
    try:
        account.receive_all()
    except:
        # Already processing
        return 0
    deposit_amount = float(account.get_balance()["balance_decimal"])
    if float(deposit_amount) >= 0.01:
        account.send(MAIN_DEPOSIT_WALLET.get_address(), str(deposit_amount))
        print(f"Deposit of {str(deposit_amount)} BAN Processed")
        return deposit_amount
    return 0


def process_withdrawal(payout_address: str, amount: float) -> bool:
    try:
        MAIN_DEPOSIT_WALLET.receive_all()
    except:
        pass
    try:
        MAIN_DEPOSIT_WALLET.send(payout_address, str(amount))
    except:
        return False
    return True


if __name__ == "__main__":
    print(new_deposit_keypair())
