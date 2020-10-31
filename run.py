def main():
    from scrape import scrape
    from do_etl import do_etl
    
    try:
        scrape()
    except ValueError as e:
        print(e)
    finally:
        do_etl(inital_load = False)

if __name__ == '__main__':
    main()