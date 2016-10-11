# distributed_scraping
Quick and dirty Django project dedicated to distributed scraping for a scalable amount of customers

Any new .py scraper can be added to utils/scraping/scrapers and will be taken into account automatically by the daemon.
Customers can get the scraped data from their personal account. Data can be sorted and downloaded (customer can decide the age of the data he is downloading). Newly scraped data are highlited.
Nice JQplot graphs make the data presentation nicer.
Customers are informed by email of the new data found by the scraper and can receive data packed in a CSV attached file or simply in HTML within the email.

This project is not complete. Some important part are still missing.

