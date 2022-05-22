#!/usr/bin/python
import sys, getopt

def main(argv):
    # get console arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["current_gas=", "tx_total_gas=", "eth_usd_price="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    current_gas = None
    tx_total_gas = None
    eth_usd_price = None
    for opt, arg in opts:
        if opt == "--current_gas":
            current_gas = arg
        elif opt in ("--tx_total_gas"):
            tx_total_gas = arg
        elif opt in ("--eth_usd_price"):
            eth_usd_price = arg
        else:
            assert False, "unhandled option"

    # calculate gas
    # 1 GWEI = 0.000000001 ETH
    cost_in_gwei = float(current_gas) * float(tx_total_gas)
    cost_in_eth = round((cost_in_gwei * 0.000000001), 4)
    cost_in_usd = cost_in_eth * float(eth_usd_price)

    print("~ cost in GWEI is: {}".format(cost_in_gwei))
    print("~ cost in ETH is: {}".format(cost_in_eth))
    print("~ cost in USD is: ${}".format(cost_in_usd))

if __name__ == "__main__":
    main(sys.argv[1:])
