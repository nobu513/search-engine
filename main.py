from data_crawler.obj.crawler import Clawler
import time

def main():
    crawler = Clawler(start_page=24)
    crawler.load()
    time.sleep(4)    
    crawler._screenshot()
    time.sleep(2)
    crawler.image_to_text()
    

if __name__ == "__main__":
    main()

