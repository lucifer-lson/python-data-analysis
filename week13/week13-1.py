"""
作者：Lucifer
日期：2023年05月27日
"""
import time
from lxml import etree
import asyncio
import aiohttp
import re
import aiofiles


class VoaCrawler:
    def __init__(self):
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/78.0.3904.97 Safari/537.36 '
            }
        self.urls = []
        for i in range(3, 4):
            self.urls.append(f'https://www.51voa.com/VOA_Standard_{i}.html')

    async def GetWeblink(self, url):
        """
        抽取单个页面的所有链接
        """
        links = []
        async with aiohttp.ClientSession() as client:
            async with await client.get(url, headers=self.headers) as rsp:
                html = etree.HTML(await rsp.text())
                for j in range(0, 50):
                    links.append(html.xpath('//*[@id="righter"]/div[3]/ul/li/a/@href'))
        return links[0]

    async def GetMp3link(self, link):
        """
        分析单个链接并得到mp3的连接
        """
        url = 'https://www.51voa.com' + link
        async with aiohttp.ClientSession() as client:
            async with client.get(url, headers=self.headers) as rsp:
                murl = re.search(r'https://.+?\.mp3', await rsp.text())
        return murl.group()

    async def SaveMp3(self, murl):
        """
        下载并保存单个mp3音频
        """
        client = aiohttp.ClientSession()
        async with client.get(murl, headers=self.headers) as rsp:
            fname = murl[murl.rfind('/') + 1:]
        async with client.get(murl, headers=self.headers) as resp:
            async with aiofiles.open(fname, 'wb') as f:
                await f.write(await resp.content.read())
                print(fname, '下载完成')
        await client.close()

    async def ATest(self, url):
        """
        对单个页面进行 链接提取-链接解析-mp3下载 全流程
        """
        links = await self.GetWeblink(url)
        print(links)
        murls = []
        for link in links:
            print(link)
            murl = await self.GetMp3link(link)
            murls.append(murl)
        for murl in murls:
            await self.SaveMp3(murl)

    def aio_main(self):
        """
        异步协程，创建事件循环
        """
        loop = asyncio.get_event_loop()
        tasks = []
        for url in self.urls:
            tasks += [self.ATest(url)]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

    def run(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 修改Windows默认设置
        self.aio_main()


if __name__ == "__main__":
    voacrawler = VoaCrawler()
    starttime = time.time()
    voacrawler.run()
    duration = time.time() - starttime
    # 打印所消耗时间
    print(f'time: {duration}')

