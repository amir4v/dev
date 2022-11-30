import os
import sys


def dir(path, indent=0):
    if indent > 1:
        return 0
    
    listdir = os.listdir(path)
    
    for p in listdir:
        p_name = p
        p = f'{path}/{p}'
        
        if '__pycache__' in p:
            continue
        
        print('----' * indent, end='')
        
        if os.path.isfile(p):
            print(p_name)
        else:
            print(p_name)
            dir(p, indent+1)


base_path = 'C:/Users/Amir/.virtualenvs/dev-QlN82kKl/Lib/site-packages/'
package_name = 'django'
path = base_path + package_name

dir(path)
