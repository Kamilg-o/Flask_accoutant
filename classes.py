import sys

class Product:
    def __init__(self,name):
        self.name= name
        self.qty = 0

class Manager:

    def __init__(self):
        self.callbacks = {}
        self.action_args = {}
        self.saldo = 0
        self.commands = []
        self.magazyn = {}
        self.count = []

    def asign(self, action, count):
        def decorate(callback):
            self.callbacks[action] = callback
            self.action_args[action] = count

        return decorate

    def create_commands(self, action_list):
        while action_list:
            action = action_list.pop(0)
            self.count.append(action)
            params = []
            # print(action_list)
            if action in self.action_args:
                for i in range(self.action_args[action]):
                    # print(i)
                    params.append(action_list.pop(0))
                self.commands.append((action, params))
            for i in params:
                self.count.append(i)

    def execute(self):
        for action, params in self.commands:
            if action in self.callbacks:
                self.callbacks[action](params)


class File:

    def __init__(self,file_pathin):
        self.file_pathin = file_pathin
        self.actions = []

    def file_reader(self,file_pathin):
        with open(self.file_pathin, "r") as file:
            for line in file:
                self.actions.append(line.strip())
# import_file = "in.txt"
mg = Manager()
# fr= File(file_pathin=import_file)

# fr.file_reader(fr.file_pathin)

@mg.asign("saldo", 2)
def saldo(params):
    value = int(params[0])
    comment = str(params[1])
    mg.saldo += value


@mg.asign("kupno", 3)
def kupno(params):
    name = params[0]
    price = params[1]
    qty = int(params[2])
    test=mg.saldo-(int(price) * int(qty))
    if test >=0:
        mg.saldo -= (int(price) * int(qty))
        if name in mg.magazyn.keys():
            mg.magazyn[name] += int(qty)
        else:
            mg.magazyn[name] = int(qty)
    else:
        mg.saldo=mg.saldo


@mg.asign("sprzedaz", 3)
def sprzedaz(params):
    name = params[0]
    price = params[1]
    qty = params[2]
    if name in mg.magazyn.keys():
        test_magazynu = mg.magazyn[name] - int(qty)
        while test_magazynu >= 0:
            mg.saldo += int(price) * int(qty)
            if name in mg.magazyn.keys():
                mg.magazyn[name] -= int(qty)
            else:
                mg.magazyn[name] = int(qty) - (2 * int(qty))
            break


