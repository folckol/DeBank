from ccxt import pro

from DeBankWarmingSystem import *

addresses = []
privates = []
proxys = []

with open('Data/Address.txt', 'r') as file:
    for i in file:

        addresses.append(i.rstrip())

with open('Data/Privates.txt', 'r') as file:
    for i in file:
        privates.append(i.rstrip())

with open('Data/Proxy.txt', 'r') as file:
    for i in file:
        proxys.append(i.rstrip())

for i in range(len(addresses)):
    newAcc = DebankAccount(id=str(uuid.uuid4()),
                           address=addresses[i],
                           privateKey=privates[i],
                           proxy=proxys[i],
                           lastChangeDate=date.fromtimestamp(1685345338)
                           )

    session.add(newAcc)
    session.commit()





