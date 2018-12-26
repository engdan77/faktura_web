Faktura web

Example usage creating docker
```
docker run -d -p 443:443 -v /tmp/faktura_db:/home/nginx/web2py/applications/faktura_web/databases --name faktura_container faktura_web && sleep 5 && docker logs fw
```