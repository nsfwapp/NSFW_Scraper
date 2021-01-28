**UPDATE** 
Scraper is working very well and supports 7 sites as the moment check supported_sites.md

# NSFW_Scraper
Scraper to get Meta-data of all available scenes and movies and storing it to Postgresql every few days.

## TODO
- [ ] find best source for performers, movies and studios
- [ ] create data model for postgres
- [ ] create data model for mongodb & update mongodb branch
- [x] created 6+ tables with relations -> scenes, performers, movies, studios, genres, tags
- [ ] fix pipeline | scrapy item isn't getting stored with scene = Scene(**item) 
- [ ] add movies from {find_website} or just link up with scene so it gets easy to link movie and it's respective scenes
- [ ] Fix vixen.com spider ( problem with scraping 7 of 319 scences)

## Goals
- First complete all todo's
- [check](https://www.writeurl.com/text/dxuu42cgxbhikxcpt62u/muflr3x9oygl98cm7skz)

## For guys who use mongodb
- use mongodb_pipeline branch [here](https://github.com/nsfwapp/NSFW_Scraper/tree/mongo-atlas_Pipeline)
