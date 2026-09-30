import asyncio


async def task_1():
    print("task 1 started")

    await asyncio.sleep(2)

    print("task 1 ended")


async def task_2():
    print("task 2 started")

    await asyncio.sleep(4)

    print("task 2 ended")


async def main():
    await asyncio.gather(task_1(), task_2())


if __name__ == "__main__":
    asyncio.run(main())