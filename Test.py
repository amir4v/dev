class C:
    def __init__(self):
        print('init')
    
    def __call__(self):
        print('call')
    
    def _get(self):
        print(str(self)+str(8778))
    
    # def __getattribute__(self, name):
    #     return self._get()


c = C()

c._get()
