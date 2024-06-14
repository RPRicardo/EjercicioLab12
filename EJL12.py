class SaldoEfectivoInsuficiente(Exception):
    pass

class SaldoCuentaInsuficiente(Exception):
    pass

class Cuenta:
    def __init__(self, id_cuenta, nombre, saldo):
        self.id_cuenta = id_cuenta
        self.nombre = nombre
        self.saldo = saldo

class CajeroAutomatico:
    def __init__(self):
        self.efectivo_disponible = 100000
        self.cuentas = {
            "1234": Cuenta("1234", "Juan Perez", 5000),
            "5678": Cuenta("5678", "Maria Gomez", 10000)
        }
        self.cuenta_actual = None

    def autenticar(self, id_cuenta):
        if id_cuenta in self.cuentas:
            self.cuenta_actual = self.cuentas[id_cuenta]
            print(f"Autenticado como {self.cuenta_actual.nombre}")
        else:
            print("Cuenta no encontrada")
    
    def mostrar_saldo(self):
        if self.cuenta_actual:
            print(f"Saldo actual: ${self.cuenta_actual.saldo}")
        else:
            print("Por favor, autentíquese primero")

    def deposito(self, monto, id_cuenta=None):
        if self.cuenta_actual:
            if id_cuenta:
                if id_cuenta in self.cuentas:
                    self.cuentas[id_cuenta].saldo += monto
                    print(f"Depósito de ${monto} a la cuenta {id_cuenta} exitoso")
                else:
                    print("Cuenta no encontrada")
            else:
                self.cuenta_actual.saldo += monto
                print(f"Depósito de ${monto} a su cuenta exitoso")
        else:
            print("Por favor, autentíquese primero")

    def transferencia(self, monto, id_cuenta_destino):
        if self.cuenta_actual:
            if id_cuenta_destino in self.cuentas:
                if self.cuenta_actual.saldo >= monto:
                    self.cuenta_actual.saldo -= monto
                    self.cuentas[id_cuenta_destino].saldo += monto
                    print(f"Transferencia de ${monto} a la cuenta {id_cuenta_destino} exitosa")
                else:
                    raise SaldoCuentaInsuficiente("Saldo insuficiente en la cuenta")
            else:
                print("Cuenta destino no encontrada")
        else:
            print("Por favor, autentíquese primero")

    def retiro(self, monto):
        if self.cuenta_actual:
            if self.efectivo_disponible >= monto:
                if self.cuenta_actual.saldo >= monto:
                    self.cuenta_actual.saldo -= monto
                    self.efectivo_disponible -= monto
                    print(f"Retiro de ${monto} exitoso")
                else:
                    raise SaldoCuentaInsuficiente("Saldo insuficiente en la cuenta")
            else:
                raise SaldoEfectivoInsuficiente("Saldo insuficiente en el cajero")
        else:
            print("Por favor, autentíquese primero")


cajero = CajeroAutomatico()
id_cuenta = input("Ingrese su ID de cuenta: ")
cajero.autenticar(id_cuenta)
cajero.mostrar_saldo()
cajero.deposito(2000)
try:
    cajero.retiro(120000)  # Intento de retirar más efectivo del disponible en el cajero
except SaldoEfectivoInsuficiente as e:
    print(e)

try:
    cajero.transferencia(6000, "5678")  # Intento de transferir más del saldo disponible en la cuenta
    cajero.mostrar_saldo()
    cajero.retiro(2000)
except SaldoCuentaInsuficiente as e:
    print(e)

