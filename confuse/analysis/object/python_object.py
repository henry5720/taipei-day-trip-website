""" Class & Instance
class GirlFriend:
    pass
gf_1=GirlFriend()
gf_2=GirlFriend()
print(gf_1)
print(gf_2)

gf_1.first_name = "Emily"
gf_1.family_name = "Li"
gf_1.email = "Emily-Li@tsinghua.edu"
gf_1.student_id = 113265

gf_2.first_name = "Cherry"
gf_2.family_name = "Wang"
gf_2.email = "Cherry-Wang@peking.edu"
gf_2.student_id = 4215652

print(gf_1.email)
print(gf_2.email)
"""

""" Variables
class GirlFriend:
    def __init__(self, first_name, family_name, university, student_id):
        self.first_name=first_name
        self.family_name=family_name
        self.university=university
        self.email=f"{first_name}-{family_name}@{university}.edu"
        self.student_id=student_id
gf_1=GirlFriend("Emily", "Li", "tsinghua", 113265)
gf_2 = GirlFriend("Cherry", "Wang", "peking", 4215652)

print(gf_1.email)
print(gf_2.email)
print(f"{gf_1.first_name} {gf_1.family_name}")
"""

""" Method Construct
class GirlFriend:
    def __init__(self, first_name, family_name, university, student_id):
        self.first_name=first_name
        self.family_name=family_name
        self.university=university
        self.email=f"{first_name}-{family_name}@{university}.edu"
        self.student_id=student_id
    def gf_name(self):
        return f"{self.first_name} {self.family_name}"

gf_1=GirlFriend("Emily", "Li", "tsinghua", 113265)
gf_2 = GirlFriend("Cherry", "Wang", "peking", 4215652)

print(gf_1.gf_name())
print(GirlFriend.gf_name(gf_2))
"""

""" Class Variables and Instance Variables
class GirlFriend():
    
    def __init__(self, first_name, family_name, university, student_id, expense):
        self.first_name = first_name
        self.family_name = family_name
        self.email = f"{first_name}-{family_name}@{university}.edu"
        self.student_id = student_id
        self.expense = expense
        GirlFriend.num_of_gf += 1
        
    def gf_name(self):

        return f"{self.first_name} {self.family_name}"
    
    def expense_incse(self):
        self.expense = int(self.expense * 1.1)

gf_1 = GirlFriend("Emily", "Li", "tsinghua", 113265, 2000)

class GirlFriend():

    incse_ratio = 1.1

    def __init__(self, first_name, family_name, university, student_id, expense):
        self.first_name = first_name
        self.family_name = family_name
        self.email = f"{first_name}-{family_name}@{university}.edu"
        self.student_id = student_id
        self.expense = expense
        
    def gf_name(self):

        return f"{self.first_name} {self.family_name}"
    
    def expense_incse(self):
        self.expense = int(self.expense * incse_ratio)

gf_1 = GirlFriend("Emily", "Li", "tsinghua", 113265, 2000)
"""

""" Inheritance and Subclass（ isinstance(), issubclass()）
"""
class GirlFriend():
    
    incse_ratio = 1.1
    
    def __init__(self, first_name, family_name, university, student_id, expense):
        self.first_name = first_name
        self.family_name = family_name
        self.email = f"{first_name}-{family_name}@{university}.edu"
        self.student_id = student_id
        self.expense = expense
        
    def gf_name(self):
        
        return f"{self.first_name} {self.family_name}"
    
    def expense_incse(self):
        self.expense = int(self.expense * self.incse_ratio)
        
class Mistress(GirlFriend):
    
    incse_ratio = 1.2
    
    def __init__(self, first_name, family_name, university, student_id, expense, job):
        super().__init__(first_name, family_name, university, student_id, expense)
        self.job = job

class Wife(GirlFriend):

    def __init__(self, first_name, family_name, university, student_id, expense, gf_lst = None):
        super().__init__(first_name, family_name, university, student_id, expense)
        
        if gf_lst is None:
            self.gf_lst = []
        else:
            self.gf_lst = gf_lst
        
    def add_gf(self, gf):
        if gf not in self.gf_lst:
            self.gf_lst.append(gf)
    
    def rmv_gf(self, gf):
        if gf in self.gf_lst:
            self.gf_lst.remove(gf)
            
    def show_gfs(self):
        for gf in self.gf_lst:
            print(f"Girl Friend: {gf.gf_name()}")
            
ms_1 = Mistress("Emily", "Li", "tsinghua", 113265, 2000, "Research Asssitant")
ms_2 = Mistress("Cherry", "Wang", "peking", 4215652, 1500, "Personal Trainer")

wf_1 = Wife("Kristy", "Huang", "shangcai", 146754, 9000, [ms_1])

print(wf_1.show_gfs())
wf_1.add_gf(ms_2)
print(wf_1.show_gfs())