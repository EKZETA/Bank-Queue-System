import os
from tabulate import tabulate
from abc import ABC, abstractmethod

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Queue:
    def __init__(self, prefix):
        self.queue = []
        self.prefix = prefix
        self.last_ticket = 0

    def generate_ticket(self):
        if self.queue:
            last_number = int(self.queue[-1][1:])
        else:
            last_number = self.last_ticket
        
        new_number = last_number + 1
        ticket = f"{self.prefix} {new_number:03}"
        self.last_ticket = new_number
        self.queue.append(ticket)
        return ticket

class ServiceCounter(ABC):
    def __init__(self, num_counters):
        self.counters = [None] * num_counters

    @abstractmethod
    def process_queue(self, queue):
        pass

    def finish_service(self, counter_id):
        if 1 <= counter_id <= len(self.counters):
            if self.counters[counter_id - 1] is not None:
                print(f"Nomor {self.counters[counter_id - 1]} telah selesai dilayani di Loket {counter_id}.")
                self.counters[counter_id - 1] = None
            else:
                print(f"Loket {counter_id} sedang kosong.")
        else:
            print("ID Loket tidak valid.")

    def show_counter_status(self, counter_type):
        table = []
        for idx, counter in enumerate(self.counters):
            table.append([f"Loket {idx + 1}", counter if counter else "Kosong"])
        print(tabulate(table, headers=[f"{counter_type} Counter", "Nomor Antrian"]))

class TellerCounter(ServiceCounter):
    def process_queue(self, queue):
        for i in range(len(self.counters)):
            if self.counters[i] is None and queue.queue:
                self.counters[i] = queue.queue.pop(0)

        table = []
        for idx, counter in enumerate(self.counters):
            table.append([f"Loket {idx + 1}", counter if counter else "Kosong"])

        print(tabulate(table, headers=["Teller Counter", "Nomor Antrian"]))
        print("\nAntrian Menunggu:")
        if queue.queue:
            for ticket in queue.queue:
                print(ticket)
        else:
            print("Tidak ada antrian.")

class CustomerServiceCounter(ServiceCounter):
    def process_queue(self, queue):
        for i in range(len(self.counters)):
            if self.counters[i] is None and queue.queue:
                self.counters[i] = queue.queue.pop(0)

        table = []
        for idx, counter in enumerate(self.counters):
            table.append([f"Loket {idx + 1}", counter if counter else "Kosong"])

        print(tabulate(table, headers=["Customer Service Counter", "Nomor Antrian"]))
        print("\nAntrian Menunggu:")
        if queue.queue:
            for ticket in queue.queue:
                print(ticket)
        else:
            print("Tidak ada antrian.")

class BankQueueSystem:
    def __init__(self):
        self.teller_queue = Queue("A")
        self.cs_queue = Queue("B")
        self.teller_counter = TellerCounter(4)
        self.cs_counter = CustomerServiceCounter(3)

    def add_to_teller_queue(self):
        ticket = self.teller_queue.generate_ticket()
        print(f"Ticket {ticket} added to Teller Queue.")

    def add_to_cs_queue(self):
        ticket = self.cs_queue.generate_ticket()
        print(f"Ticket {ticket} added to Customer Service Queue.")

    def show_teller_queue(self):
        print("\n=== Antrian Teller ===")
        self.teller_counter.process_queue(self.teller_queue)

    def show_cs_queue(self):
        print("\n=== Antrian Customer Service ===")
        self.cs_counter.process_queue(self.cs_queue)

    def main_menu(self):
        while True:
            clear_screen()
            print("\n=== Sistem Antrian Bank ===")
            print("1. Tambah Antrian Teller")
            print("2. Tambah Antrian Customer Service")
            print("3. Lihat Antrian Teller")
            print("4. Lihat Antrian Customer Service")
            print("5. Selesaikan Layanan Teller")
            print("6. Selesaikan Layanan Customer Service")
            print("7. Keluar")

            try:
                choice = int(input("Pilih menu: "))
                if choice == 1:
                    self.add_to_teller_queue()
                elif choice == 2:
                    self.add_to_cs_queue()
                elif choice == 3:
                    self.show_teller_queue()
                elif choice == 4:
                    self.show_cs_queue()
                elif choice == 5:
                    counter_id = int(input("Masukkan ID Loket yang ingin diselesaikan (1-4): "))
                    self.teller_counter.finish_service(counter_id)
                elif choice == 6:
                    counter_id = int(input("Masukkan ID Loket yang ingin diselesaikan (1-3): "))
                    self.cs_counter.finish_service(counter_id)
                elif choice == 7:
                    print("Keluar dari sistem.")
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid, masukkan angka.")

            input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    system = BankQueueSystem()
    system.main_menu()