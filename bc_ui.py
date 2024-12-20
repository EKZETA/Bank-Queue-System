import streamlit as st
from tabulate import tabulate

class BankQueueSystem:
    def __init__(self):
        self.teller_queue = []  # List for teller queue
        self.cs_queue = []  # List for customer service queue
        self.teller_counters = [None] * 4  # Represent 4 teller counters
        self.cs_counters = [None] * 3  # Represent 3 customer service counters

    def generate_ticket(self, queue, prefix):
        """Generate a new ticket number"""
        if queue:
            last_number = int(queue[-1][1:])
        else:
            last_number = 0
        new_number = f"{prefix} {last_number + 1:03}"
        return new_number

    def add_to_teller_queue(self):
        ticket = self.generate_ticket(self.teller_queue, "A")
        self.teller_queue.append(ticket)
        return ticket

    def add_to_cs_queue(self):
        ticket = self.generate_ticket(self.cs_queue, "B")
        self.cs_queue.append(ticket)
        return ticket

    def process_queue(self, queue, counters):
        """Process a queue and assign tickets to counters."""
        for i in range(len(counters)):
            if counters[i] is None and queue:
                counters[i] = queue.pop(0)
        return counters

    def finish_service(self, counters, counter_id):
        """Mark the service as finished."""
        if 1 <= counter_id <= len(counters):
            if counters[counter_id - 1] is not None:
                counters[counter_id - 1] = None
                return True
        return False

    def get_queue_status(self, queue, counters):
        """Get the current status of the queue and counters."""
        waiting_tickets = queue
        counter_status = [counter if counter else "Kosong" for counter in counters]
        return waiting_tickets, counter_status

# Initialize the system
if 'bank_system' not in st.session_state:
    st.session_state.bank_system = BankQueueSystem()

bank_system = st.session_state.bank_system

# Streamlit app UI
st.title("Sistem Antrian Bank")

menu = st.sidebar.radio("Menu", ["Tambah Antrian", "Lihat Antrian", "Selesaikan Layanan"])

if menu == "Tambah Antrian":
    st.header("Tambah Antrian")
    option = st.radio("Pilih jenis antrian:", ["Teller", "Customer Service"])

    if st.button("Tambah Antrian"):
        if option == "Teller":
            ticket = bank_system.add_to_teller_queue()
            st.success(f"Nomor antrian {ticket} ditambahkan ke Teller Queue.")
        else:
            ticket = bank_system.add_to_cs_queue()
            st.success(f"Nomor antrian {ticket} ditambahkan ke Customer Service Queue.")

elif menu == "Lihat Antrian":
    st.header("Lihat Antrian")
    option = st.radio("Pilih jenis antrian:", ["Teller", "Customer Service"])

    if option == "Teller":
        bank_system.process_queue(bank_system.teller_queue, bank_system.teller_counters)
        queue, counters = bank_system.get_queue_status(bank_system.teller_queue, bank_system.teller_counters)
    else:
        bank_system.process_queue(bank_system.cs_queue, bank_system.cs_counters)
        queue, counters = bank_system.get_queue_status(bank_system.cs_queue, bank_system.cs_counters)

    st.subheader("Status Loket")
    for idx, counter in enumerate(counters):
        st.write(f"Loket {idx + 1}: {counter}")

    st.subheader("Antrian Menunggu")
    if queue:
        for ticket in queue:
            st.write(ticket)
    else:
        st.write("Tidak ada antrian.")

elif menu == "Selesaikan Layanan":
    st.header("Selesaikan Layanan")
    option = st.radio("Pilih jenis antrian:", ["Teller", "Customer Service"])

    if option == "Teller":
        counters = bank_system.teller_counters
    else:
        counters = bank_system.cs_counters

    st.subheader("Status Loket")
    for idx, counter in enumerate(counters):
        st.write(f"Loket {idx + 1}: {counter if counter else 'Kosong'}")

    counter_id = st.number_input("Masukkan ID Loket yang ingin diselesaikan:", min_value=1, max_value=len(counters), step=1)
    if st.button("Selesaikan Layanan"):
        if bank_system.finish_service(counters, int(counter_id)):
            st.success(f"Layanan di Loket {counter_id} selesai.")
        else:
            st.error(f"Loket {counter_id} sedang kosong atau ID tidak valid.")