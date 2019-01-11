# Faktura Web

My father-in-law asked for an easy-to-use application for keep record of invoices for his clients in Swedish, and could not find any so this became a quick project to pull this together that other might find useful as a base foundation.

Basic functions
* Create company, products, clients
* Maintain invoice with due-date payments
* Print invoice as PDF

![alt faktura_web_demo](https://i.imgflip.com/2qvlaa.gif)

## Installation

```bash
git clone && cd faktura_web
docker build . --tag faktura_web_image
docker run -d -p 443:443 -v [LOCAL DATABASE FOLDER]:/home/nginx/web2py/applications/faktura_web/databases --name faktura_web_container faktura_web_image && sleep 5 && docker logs faktura_web_container
```

## Usage

Go to either

`https://[Docker IP]`
 
for accessing faktura_web 

`https://[Docker IP]/admin` 

(default password: admin) 

for accessing web2py built-in admin page

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Database model

![alt db_model](https://i.imgflip.com/2qvmcb.gif)