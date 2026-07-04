import asyncio
from agent import Coordinator
from utils.cli import *
coordinator = Coordinator()


async def main():

    while True:
        
        user()
        query = input()

        if query in ["exit", "quit"]:
            break

        result = await coordinator.chat(query)
        
        final(result)


if __name__ == "__main__":
    asyncio.run(main())