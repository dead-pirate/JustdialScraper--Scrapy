import scrapy
import json

class jdscrap(scrapy.Spider):
    name="justdial"

    allowed_domains = ["justdial.com"]


    req_url= [ "https://www.justdial.com/functions/ajxsearch.php?national_search=0&act=pagination_new&city=Delhi&search=House On Rent&where=&catid=0&psearch=&prid=&page=%s&SID=&mntypgrp=0&toknbkt=&bookDate=&jdsrc=&median_latitude=28.664407557287&median_longitude=77.090145924828&ncatid=10192844&mncatname=Estate Agents For Residential Rental&dcity=Delhi&pncode=999999&htlis=0" %i for i in range(2,11)]

    start_urls = [
                    "https://www.justdial.com/Delhi/House-On-Rent/nct-10192844"
                    ]

    handle_httpstatus_list = [403]
    download_delay = 3

    def start_requests(self):
                    
                    #get the header data from network tab in web dev tools(ctrl+shift+i)
        headers = { "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "dnt": "1",
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "authority": "www.justdial.com",
                    "method": "GET",
                    "origin": "https://www.justdial.com",
                    "referer": "https://www.justdial.com/Delhi/House-On-Rent/nct-10192844",
                    "cookie": """ppc=; TKY=77253a16ef0f1116b5dac4f27f49988ca89c0c080043a397a148cf7ec690eac5; _ctok=891b54e135c17b36c8ec35184e6b0ff55d575fa47b7a89bc57b51e224583d245; attn_user=logout; ppc=; _ga=GA1.2.1206336958.1595598782; _gid=GA1.2.942785449.1595598782; usrcity=Mumbai; profbd=0; bdcheck=1; tab=toprs; bd_inputs=2|4|Estate%20Agents%20For%20Residential%20Rental; view=lst_v; sarea=; scity=Delhi; dealBackCity=Delhi; prevcatid=10192844; BDprofile=1; detailmodule=011PXX11.XX11.160222143234.U4K8; docidarray=%7B%22011PXX11.XX11.160222143234.U4K8%22%3A%222020-07-25%22%7D; PHPSESSID=558342d0cbdc4df9d32401ea728b5b00; main_city=Delhi; akcty=Delhi; inweb_city=Delhi; ak_bmsc=4CEBBC1188CBB24EAC096B1813C30E40312C755715390000E8551C5F4866CD1C~plLou8/mwQBuW48dQqc7WldlczFFPqyAFkv6eJ2XdoKagoRu+82Iz8IrxJu1EA7xhmDjF90+MCZCUJ2FECn3JnZrqj185Vkskur+CbtrYVZTM6K+GD0Cejl8NGWkcCkPNIKh8+I5OqvRGBe7fn85aZPoU951GzXOg7PjRHrCJTYYSRVvYqfKjG6wp92Qff4OkaMvoGYqhB8NYxUeDlQxQjKVx9i0oBFTxZ985Qm3vkjWlCavAvDBGUy+GclTQdP4IbP+IRuFgzWPWq7U/jcugG9A==; bm_sv=ED109623B2DB34EA43AD22880DB6D8D1~kZwcEGn9UE6mx+/2I3KA5HO4u9Q+kDArt38Pzx2CyPfHfAdkY0NIIYAWsMDk8RsI+0/L3iwHDtwfxDdDTQ4PU4hl9v1U9iZP+m1Q84jg7WBuPo7lNRhXtw95zalcpdQsWUaWpdXn/s9hc7jpelWfmRj/r8rdyRGEgq62ubSgU24=""",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-frsc-token": "77253a16ef0f1116b5dac4f27f49988ca89c0c080043a397a148cf7ec690eac5",
                    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest"


                    }

#        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                headers = headers
                            )
        for url in self.req_url:
            yield scrapy.Request(url=url, callback=self.parse2,
                                headers = headers )



    def getphone(self,ph_arr):

        digit={"dc":"+" , "fe":"(" , "hg":")" , "ba":"-" , "acb":"0" , "yz":"1",
                "wx":"2" ,"vu":"3" , "ts":"4" , "rq":"5" , "po":"6" , "nm":"7" ,
                "lk":"8" , "ji":"9"}
        ph = []

        for i in ph_arr:
            ph.append( digit.get(
            i.replace('mobilesv','').replace('icon-','').replace(' ' ,'')))

        return ''.join(ph)


    def parse(self,response):

        for post in response.css("li.cntanr "):

            yield{

                'Name': post.css("span.lng_cont_name ::text").get(),
                'Rating':post.css("span.exrt_count  ::text").get(),
                'Phone': self.getphone(post.css("p.contact-info span::attr(class)").getall()),
                'Address':post.css("span.cont_sw_addr ::text").get().replace('\t','').replace('\n','')

            }

    def parse2(self,response):

        try:
            json_data = json.loads(response.text)                              #loading the json data
            selector = scrapy.Selector(text = json_data.get('markup'))         #converting the html inside json_data to Selector type
            #print(json_data.keys())


            for post in selector.css("li.cntanr "):

                yield{

                    'Name': post.css("span.lng_cont_name ::text").get(),
                    'Rating':post.css("span.exrt_count  ::text").get(),
                    'Phone': self.getphone(post.css("p.contact-info span::attr(class)").getall()),
                    'Address':post.css("span.cont_sw_addr ::text").get().replace('\t','').replace('\n','')

                }
        except:
            pass


            #scrapy crawl name -o filename.json
