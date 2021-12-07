from data_crawler.obj.crawler import Clawler

def main():
    crawler = Clawler(start_page=5)
    crawler.load()
    

if __name__ == "__main__":
    main()

