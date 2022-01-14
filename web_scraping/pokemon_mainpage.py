import scrapy


def _parse_int_or_0(val):
    try:
        return int(val)
    except ValueError:
        return 0


class PokemonMainpageSpider(scrapy.Spider):
    name = "pokemon_mainpage"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/"]

    def parse(self, response):
        links = response.css("a.type-icon::attr(href)").getall()
        for type_page_link in links:
            type_page = response.urljoin(type_page_link)
            yield scrapy.Request(type_page, callback=self.parse_type_page)

    def parse_type_page(self, response):
        pokepage_links = response.css("div.infocard a.ent-name::attr(href)").getall()
        for poke_link in pokepage_links:
            pokemon_page = response.urljoin(poke_link)
            yield scrapy.Request(
                pokemon_page,
                callback=self.parse_pokemon_page,
            )

    def parse_pokemon_page(self, response):
        # find number
        pokedex_data_table = response.xpath(
            "//div[h2[contains(text(), 'Pokédex data')]]//table"
        )
        pokemon_number = pokedex_data_table.css("strong::text").get()

        # parse attributes
        attributes = {}
        tbody = response.xpath(
            "//div[h2[contains(text(), 'Base stats')]]/div/table/tbody"
        )
        for row in tbody.css("tr"):
            attribute = row.css("th::text").get()  # e.g 'HP', 'Attack'
            start, min, max = row.css("td.cell-num::text").getall()

            attributes[attribute] = {
                "start": int(start),
                "min": int(min),
                "max": int(max),
            }

        # get move by level
        moves = []
        moves_tbody = response.xpath(
            "//div[h3[contains(text(), 'Moves learnt by level up')]]/div/table/tbody"
        )
        for row in moves_tbody[0].css("tr"):
            move_name = row.css("td.cell-name a::text").get()
            level, power, acc = row.css("td.cell-num::text").getall()
            type = row.css("td.cell-icon a::text").get()
            category = row.css("td.cell-icon img::attr(alt)").get()
            move = {
                "name": move_name,
                "level": int(level),
                "power": _parse_int_or_0(power),
                "accuracy": _parse_int_or_0(acc),
                "type": type,
                "category": category,
            }
            moves.append(move)

        # store data about this pokemon
        data = {
            "attributes": attributes,
            "name": response.css("main#main h1::text").get(),
            "number": int(pokemon_number),
            "moves": moves,
        }
        yield data

