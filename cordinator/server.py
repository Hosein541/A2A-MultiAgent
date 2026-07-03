import asyncio
from agent2 import Coordinator

coordinator = Coordinator()


async def main():

    while True:

        query = input("User: ")

        if query in ["exit", "quit"]:
            break

        result = await coordinator.chat(query)

        print("\nAssistant:", result, "\n")


if __name__ == "__main__":
    asyncio.run(main())