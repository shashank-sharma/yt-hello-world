# yt hello world

Sample project to understand how Youtube Search Data API works

## Technologies

1. Flask
2. PostgreSQL (latest)
3. Celery 5.x
   a. Worker - Async execution
   b. Beat - For scheduling / periodic execution
4. Redis

## Implementation

Given project is divided into multiple files and can be visualized as:

1. app.py is main file which contains all the app endpoints and celery task defined
2. models.py contain schema for YTSearch table with necessary table with video_id as primary key
3. manage.py is responsible for migration of models and making changes to postgreSQL.
4. middleware.py contains one decorator function, which checks if given parameters were passed to endpoint or not
5. errors.py has only one custom exception defined
6. flask_celery.py is there to initialize Celery object and necessary configuration
7. config.py has configuration objects to help manage configuration for different environments to work with
8. util.py is main file for Youtube API logic, it has builder to help create Youtube API object and use it
9. start.sh, simple script to migrate the changes and run flask server

Dockerization process is working by docker compose file and having 2 Docker files for web service and worker service in celery-queue directory. In total it consist of 5 services
1. db - Database
2. web - Flask
3. worker - Celery
4. beat - Celery
5. redis - Message broker

## How to run ?

1. Finalize all environment variables and define it in `.env`

For local testing, set `APP_SETTINGS` to `config.DevConfig` and necessary values for:

```
DEV_DATABASE_URL=postgresql://admin:password@localhost:5432/fpdb
DEV_BROKER_URL=redis://localhost:6379/0
DEV_RESULT_BACKEND=redis://localhost:6379/0
```

For docker builds, use PROD_<xyz> key/value pair and `APP_SETTINGS` to `config.ProdConfig`

And do specify `YT_KEY` which is youtube api secret key. For multiple keys, seperate it by single empty space

2. Once done, for local testing do:

```
python manage.py db upgrade
python app.py
```

for docker build do:

```
docker-compose up -d --build
```

## Testing

Flask server will run at: `0.0.0.0:5000``

Available endpoints are:

1. /ping: GET - Just to test if it is working
2. /search: POST -`takes 3 parameters in JSON body as:

```
{
    "search": "anime", // Query to be searched in youtube
    "page": 3,         // Pagination page
    "per_page": 2      // results per request
}
```

Response:

```
{
    "data": [
        {
            "channel_id": "UCIlu5tkUluhyMblE0Sj8IpA",
            "channel_title": "ElemperadormaxiYT",
            "description": "Conviértete en miembro de este canal para disfrutar de ventajas exclusiva como: º Agregarte de amigos º Rango especial en discord º Grabar conmigo y mas..",
            "published_at": "Tue, 09 Feb 2021 17:58:39 GMT",
            "published_time": "Tue, 09 Feb 2021 17:58:39 GMT",
            "thumbnail": "https://i.ytimg.com/vi/GbBAbBS67W4/default.jpg",
            "title": "NUEVO CODIGO DE ANIME FIGHTING SIMULATOR CODES ROBLOX * DIMENSION 5* ACTUALIZACION CODE",
            "video_id": "GbBAbBS67W4"
        },
        {
            "channel_id": "UC_WEz0p-5Ky30OORSfPubmA",
            "channel_title": "Squally",
            "description": "New FREE Epic + New Lucky Draw & New Anime Crate! Cod Mobile Leaks! Leak Credit - Dogebeanie https://youtube.com/c/dogebeanie Leak Credit - Data ...",
            "published_at": "Tue, 09 Feb 2021 17:58:39 GMT",
            "published_time": "Tue, 09 Feb 2021 17:58:39 GMT",
            "thumbnail": "https://i.ytimg.com/vi/OihPW6uNIfw/default.jpg",
            "title": "New FREE Epic + New Lucky Draw &amp; New Anime Crate! Cod Mobile Leaks!",
            "video_id": "OihPW6uNIfw"
        }
    ],
    "has_next": true,
    "has_prev": true,
    "length": 2,
    "next_page": 4,
    "prev_page": 2
}
```

3. /list: GET - Get all data in pagination. Available parameters are `per_page` and `page`

http://localhost:5000/list?per_page=2&page=2

Response:
```
{
    "data": [
        {
            "channel_id": "UCClK5D4DrAihWMeMaSA1rpA",
            "channel_title": "Everbloom Games",
            "description": "Learn More: https://everbloomgames.com/maps/anime-mash-up/ Explore a massive anime city! Our city features a giant robot boss battle, detailed interiors, ...",
            "published_at": "Tue, 09 Feb 2021 18:18:18 GMT",
            "published_time": "Tue, 09 Feb 2021 18:18:18 GMT",
            "thumbnail": "https://i.ytimg.com/vi/NtY9lHDBXIA/default.jpg",
            "title": "Anime Mash-up - Minecraft Marketplace Mash-up Trailer",
            "video_id": "NtY9lHDBXIA"
        },
        {
            "channel_id": "UCF-viuvv9jqcsWBKTkCZiQw",
            "channel_title": "Guibel Reviews",
            "description": "Bienvenidos a mi canal! TWITCH: https://www.twitch.tv/guibelreviewsli​​​​... PATREON PICANTE: https://www.patreon.com/guibelreviews​​​​... Esperamos ...",
            "published_at": "Tue, 09 Feb 2021 18:00:13 GMT",
            "published_time": "Tue, 09 Feb 2021 18:00:13 GMT",
            "thumbnail": "https://i.ytimg.com/vi/wUgxh8Px074/default.jpg",
            "title": "LOS PEORES AMIGOS EN LA HISTORIA DEL ANIME",
            "video_id": "wUgxh8Px074"
        }
    ],
    "has_next": true,
    "has_prev": true,
    "length": 2,
    "next_page": 3,
    "prev_page": 1
}
```
