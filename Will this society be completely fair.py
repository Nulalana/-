import random as r
import matplotlib.pyplot as plt

class Community:
    def __init__(self, population, transaction_price, tax_rate) -> None:
        self.population = population
        self.transaction_price = transaction_price
        self.PS = self.set_PS()
        self.tax_rate = tax_rate
        self.total_tax = 0
        self.list_citizens = [self.Citizen(self) for _ in range(self.population)]
    
    def set_PS(self):
        list_PS = [0, 1, 2]
        return r.choice(list_PS)

    def run_model(self, times):
        for _ in range(times):
            for i in range(len(self.list_citizens)-1):
                r.shuffle(self.list_citizens)
                self.list_citizens[i].consume()
                self.list_citizens[i+1].serve()

    def insolvency_assistance(self):                        # 手动调用
        assistance_fond = self.total_tax
        while assistance_fond > 0:
            for citizen in self.list_citizens:
                if citizen.asset < 0:
                    assistance_fond += citizen.asset
                    citizen.asset = 0                       # 怎么既调用这个功能又能在外部返回assistance_fond

    def show_asset(self):
        list_asset = [round(citizen.asset, 2) for citizen in self.list_citizens]
        print(sorted(list_asset, reverse=True))

    def remove_poor_citizen(self):                          
        for citizen in self.list_citizens:
            if citizen.asset <= 0:
                self.list_citizens.remove(citizen)

    class Citizen():              
        def __init__(self, Community_instance) -> None:
            self.Community_instance = Community_instance
            self.id = self.set_id()
            self.asset = 100 

        def set_id(self):
            list_id = [r.randint(100000, 1000000) for _ in range(100)]
            id = r.choice(list_id)
            return id

        def consume(self):
            self.asset -= self.Community_instance.transaction_price
            self.asset -= self.Community_instance.PS

        def serve(self):
            self.asset += self.Community_instance.transaction_price * (1 - self.Community_instance.tax_rate)
            self.Community_instance.total_tax += self.Community_instance.transaction_price * self.Community_instance.tax_rate

        def get_asset(self):
            print(self.asset)

    class Taxpayers(Citizen):                           # 收税和税率应该是属于Community中的属性，而不是Taxoayers的属性。
        def __init__(self, Community_instance) -> None:
            super().__init__(Community_instance)


community1 = Community(20, 10, 0.02)       # population, transaction_price, tax_rate
community1.run_model(30)                 # running times  
community1.insolvency_assistance() 
community1.remove_poor_citizen()     
# community1.show_asset()


all = 0
for i in range(1000):
    all += len(community1.list_citizens)
print(all)



PS_values = [citizen.Community_instance.PS for citizen in community1.list_citizens]
asset_values = [citizen.asset for citizen in community1.list_citizens]

plt.scatter(PS_values, asset_values)
plt.xlabel('PS')
plt.ylabel('Asset')
plt.title('PS vs Asset')
# plt.show()