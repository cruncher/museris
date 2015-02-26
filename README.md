# Museris

Data models and scraper for <a href="https://museris.lausanne.ch/">museris.lausanne.ch</a> developed in the context of the <a href="http://make.opendata.ch/wiki/event:2015-02">2015 Swiss Open Cultural Data Hackathon</a>.



# Installation

* Create a new virtualenv and install the requirements
* `pip install git+https://github.com/cruncher/museris.git#egg=museris-dev`
* add `numeris_data` to your `INSTALLED_APPS` settings.
* import an existing database or `python manage.py migrate` and start scraping

# Scraping

* `python manage.py scrape_data` to scrape all 180'000+ Objects
* or `python manage.py scrape_data <start_id> <end_id>` to scrape a subset of Objects
* or `python manage.py scrape_data <ID>` to scrape a single Object

Note: Object images inside `DataObjectImage` are not automatically downloaded, only the image URL is recorded. To sync and download the actual images, run `python manage.py get_object_images`

# Data models

Defined in `models.py`.

* `Institution`s are basically museums
* `DataObject`s hold infomration about a single object (paintings, physical objects, …) referenced in the museums. Has a foreign-key to an `Institution`.
* `Person`: represents a Person involved with `DataObjects` (authors, artists, photographs, curators, …)
* `DataObjectImage` hold images (urls and actual images) related to a single `DataObject`
* `DataObjectProperty` hold a single key (e.g. "Creation year") and value (e.g. "2001") related to a single `DataObject`
* `PersonProperty` same as `DataObjectProperty` but for `Person`s, e.g. "date of birth", "bio", …
* `DataObjectLatLong` hod a latitude / longitude pair for a single `DataObject`, if the object has geographic information
* `DataObjectPerson` a many-to-many relation between `DataObject`s and `Person` including a role (e.g. "Author", "Curator", …)


## Limitations and possible improvements

* Images associated to `Person`s are currently not being scraped
* Only the first image associated to each `DataObject` is downloaded, even thought there are possibly more.

# Copyright

Most objects and images in the Museris database are covered by copyright and may not be re-used. 
