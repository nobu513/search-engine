from data_crawler.obj.crawler import Clawler
import time

def main():
    crawler = Clawler(start_page=18, end_page=1632)
    crawler.start_crawler()


if __name__ == "__main__":
    main()

