from SSHAction import *

import asyncio
async def main():
    devops_engineer = DevOpsEngineer()
    await devops_engineer.act("docker ps")

if __name__ == "__main__":
    asyncio.run(main())

