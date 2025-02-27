import random

#Constants
CHECKOUT_TIME = 4
OVERHEAD_TIME = 45
CUSTOMER_ENTER_LINE = 30
SIMULATION_DURATION = 7200
EXPRESS_LINE_ITEM_LIMIT = 10
DISPLAY_INTERVAL = 50    #With a Display Interval of 50 seconds, it is very difficult to see what is happening, for testing purposes, this constant was set to 2000
SIMULATION_RUNS = 12

def main():
    print("Running Simulation 12 times (5 Registers: 1 Express, 4 Regular)")
    
    for sim in range(SIMULATION_RUNS):
        print(f'------ Simulation Run #{sim+1} ------')
        express_register = Register(True)
        regular_registers = [Register() for i in range(4)]
        run_simulation(express_register, regular_registers)
        
    print("The store is sufficiently staffed with average wait times rarely exceeding 45 seconds.\n")
    print("Nonetheless, let's see how an extra register helps out.\n")
        
    print("Running Simulation with an additional non-express register")
    
    express_register = Register(True)
    regular_registers = [Register() for i in range(5)]
    run_simulation(express_register, regular_registers)


class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    def peek(self):
        return [customer.items for customer in reversed(self.items)]     


class Customer:
    
    def __init__(self):
        self.items = random.randint(6, 20)
        self.checkout_time = self.items * CHECKOUT_TIME + OVERHEAD_TIME


class Register:
    
    def __init__(self, is_express=False):
        self.is_express = is_express
        self.queue = Queue()
        self.current_customer = None
        self.time_remaining = 0
        self.total_customers_served = 0
        self.total_items_served = 0
        self.total_idle_time = 0
        self.total_wait_time = 0
    
    def add_customer(self, customer):
        self.queue.enqueue(customer)
        
        
    def checkout(self):
        #If there is no current customer but someone is waiting in the queue, this makes them current customer
        if self.idle() and not self.queue.isEmpty():
            self.current_customer = self.queue.dequeue()
            self.time_remaining = self.current_customer.checkout_time
            self.total_customers_served += 1
            self.total_items_served += self.current_customer.items
        
        #If there is a current customer
        if self.current_customer:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_customer = None
        
        #if there is no current customer and no on waiting in the queue
        if self.idle():
            self.total_idle_time += 1
        
        #If There is someone waiting in the queue
        if not self.queue.isEmpty():
            self.total_wait_time += 1
    
    def idle(self):
        return (self.current_customer == None)
    
    def queue_size(self):
        return self.queue.size()
        
    
    def __str__(self):
        return (f"Total Customers Served: {self.total_customers_served}\n"
        f"Total Items Served: {self.total_items_served}\n"
        f"Idle Time: {self.total_idle_time}\nWait Time: {self.total_wait_time}")
    
  
#Finds the Register with the smallest queue size, breaks ties randomly
def find_minimum_register(registers_list):
    min_register = min(register.queue_size() for register in registers_list)
    candidates = [register for register in registers_list if register.queue_size() == min_register]
    return random.choice(candidates)

#This is how we pick which register a customer will go to based on the customers self.items and the queue size of each register     
def pick_register(customer, express_register, regular_registers, all_registers):
    #Express Lane Instance
    if customer.items < EXPRESS_LINE_ITEM_LIMIT:
        
        #If express register is idle and no one's waiting in line
        if express_register.idle() and express_register.queue_size() == 0:
            express_register.add_customer(customer)
        #Picks the register with the shortest queue
        else:
            minimum_register = find_minimum_register(all_registers)
            minimum_register.add_customer(customer)
            
    #Regular Instace
    elif customer.items >= EXPRESS_LINE_ITEM_LIMIT:
        minimum_register = find_minimum_register(regular_registers)
        minimum_register.add_customer(customer)


def run_simulation(express_register, regular_registers):
    
    all_registers = [express_register] + regular_registers
    
    for current_second in range(SIMULATION_DURATION):
        
        #Every 30 seconds a customer is initialized and picks a register
        if current_second % CUSTOMER_ENTER_LINE == 0:
            customer = Customer()
            pick_register(customer, express_register, regular_registers, all_registers)
            
        #Every register goes through the checkout process
        for register in all_registers:
            register.checkout()
            
            
        i = 0
        if current_second % DISPLAY_INTERVAL == 0:
            print(f"Time = {current_second}\n"
                  f"Reg#    customers\n")
            for register in all_registers:
                if register.queue.isEmpty():
                    print(f"  {i}     {register.current_customer.items if register.current_customer else '--'}" ) 
                else:
                    print(f"  {i}     {register.current_customer.items if register.current_customer else '--'} | {register.queue.peek()}" )
                i += 1
            
     
    
    i = 0  
    print('Express')
    registers_total_customers = 0
    registers_total_items = 0
    registers_total_idle_time = 0     
    for register in all_registers:
        average_wait = int(register.total_wait_time / register.total_customers_served) 
        print(f"Register       Total Customers       Total Items       Total Idle Time(min)       Average Wait Time (sec)")
        print(
            f"    {i}                   {register.total_customers_served}                   "
            f"{register.total_items_served}                  {register.total_idle_time / 60:.2f}                       "
            f"{average_wait}\n"
        )
        registers_total_customers += register.total_customers_served
        registers_total_items += register.total_items_served
        registers_total_idle_time += register.total_idle_time
        i += 1
    print('--------------------------------------------------------------------------------')
    print(f"TOTAL:                 {registers_total_customers}                   "
          f"{registers_total_items}                 {registers_total_idle_time / 60:.2f}")
main()









