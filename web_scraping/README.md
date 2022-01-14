# Pokemon scraper

In this directory we have two files:

1. `pokemon_mainpage.py`: This is the spider we defined in class for scraping the data from https://pokemondb.net You can load this into your scrapy project and call crawl to generate the data
2. `data.json`: this is the data gathered by the scraper itself


The way the scraper works is as follows:

1. Starts at `start_urls`, which is https://pokemondb.net
2. Collects the content of that page and stores it in a variable `response` and calls our `parse` method with the response.
3. Our `parse` method will then look for the section of links to the pokemon type pages. It will find all the links and for each of them it will create a new `scrapy.Request`, which tells scrapy to visit each of the pages
4. The `scrapy.Request` has a callback `self.parse_type_page`. For each type page, scrapy will fill a `response` object with the content of the page and then call this method
5. Inside `self.parse_type_page` we find a link to each pokemon of that type. Again we generate a `scrapy.Request` and this time set the callback to `self.parse_pokemon_page`
6. The `parse_pokemon_page` method has all the actual data extraction. We get the name, number, attribute list, and move list from the pokemon detail page. We store these in a dictionary and `yield` them
7. When we call `scrapy crawl pokemon_mainpage -o data.json`, scrapy will populate data.json with a list of dictionaries. Each dictionary will have the data for a single pokemon that we extracted in the previous step.


## Notes

We ran a few commands to get things setup. These are:

```
conda create -n pokemon python=3.9

conda activate pokemon

pip install scrapy

scrapy startproject pokemondb

cd pokemondb

scrapy genspider pokemon_mainpage pokemondb.net

scrapy shell https://pokemondb.net/

scrapy runspider pokemondb/spiders/pokemon_mainpage.py


```

When we use `scrapy crawl pokemon_mainpage -o data.json`, the data is *appended* to the existing data.json file. This causes problems. So, each time we want to run our scraper we first delete data.json and then call `scrapy crawl`
