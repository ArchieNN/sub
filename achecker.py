import asyncio
from aiohttp import ClientSession, ClientConnectorError
import xmltodict
#Sems ve Klaxxon tarafından itina ile kodlanmıştır


async def fetch_html(url: str, session: ClientSession):
	try:
		resp = await session.request(method="GET", url=url, timeout=3)
	except:
		return "problem"
	return (await resp.text(), resp.url, resp.status)

async def make_requests(urls):
	async with ClientSession() as session:
		for i, url in enumerate(urls):
			print(f"try count {i+1}: "+url,end="")
			result = await fetch_html(url, session)
			if result == "problem":
				print("-> Bu domaine bağlanılamıyor.")
				continue
			elif "<!doctype>" in result[0].lower() or "<html>" in result[0].lower():
				print("-> Burası html dönütü verdi.")
				continue
			elif result[2] != 403:
				print("-> 403 dönmüyor")
				continue
			resp_raw = result[0]
			resp_dict = xmltodict.parse(resp_raw)
			if "Error" in resp_dict and resp_dict["Error"]["Code"] == "AccessDenied":
				print("-> Sömürülmeye müsait gözükmekte")
				url = str(result[1])
				print(url + " | Akamai vuln found")
				open("akamai.txt", "a").write(url + "\n")
if __name__ == "__main__":
	import pathlib
	here = pathlib.Path(__file__).parent
	load = input("Taranıcak siteleri uzatın  > ")
	try:
		with open(here.joinpath(load)) as infile:
			urls = [x if x.startswith("http") else "http://"+x for x in infile.read().strip().splitlines()]
	except FileNotFoundError:
		print("Böyle bir dosya yok")

	asyncio.get_event_loop().run_until_complete((make_requests(urls)))

