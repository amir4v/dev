import asyncio

async def my_function():
    print(1)
    await asyncio.sleep(1)
    print(2)

async def your_function():
    await my_function()
    print(3)

async def our_function():
    task1 = asyncio.create_task(your_function())
    value1 = await task1
    await my_function()
    
    task2 = your_function()
    value2 = await task2
    
    results = await asyncio.gather( my_function() , your_function() )
    for result in results:
        print(result)
    
    results = asyncio.gather( my_function() , your_function() )
    for result in results:
        result = await result
        print(result)
    
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            task = tg.create_task( my_function(i) )
            tasks.append(task)
    for task in tasks:
        print( task.result() )

#
async def set_future_result(future, value):
    await asyncio.sleep(3)
    future.set_result(value)
    print(f'Set the future result to {value}')

async def main():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    asyncio.create_task( set_future_result(future, 'the value') )
    result = await future
    print(f'the result {result}')
#

#
shared_resource = 0
lock = asyncio.Lock()

async def modify_shared_resource():
    global shared_resource
    async with lock:
        shared_resource += 1
        await asyncio.sleep(3)

async def main():
    await asyncio.gather( *(modify_shared_resource() for _ in range(5)) )
#

# Semaphore (access at a resource up to a limited amount of accessibility)
async def access_resource(semaphore, res):
    async with semaphore:
        print(f'Access {res}')
        await asyncio.sleep(1)
        print(f'Refresh {res}')

async def main():
    semaphore = asyncio.Semaphore(2) # Two at a time
    await asyncio.gather( *(access_resource(i) for i in range(5)) )
#

# Event
async def waiter(event):
    print('waiting')
    await event.wait()
    print('event has been set. continuing...')

async def setter(event):
    await asyncio.sleep(2)
    event.set()
    print('event has been set')

async def main():
    event = asyncio.Event()
    await asyncio.gather( waiter(event) , setter(event) )
#

asyncio.run(our_function())
