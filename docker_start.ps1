docker compose down

$src = ".\NginxVideo\mp4\"
$dst = ".\NginxVideo\www\html"

$db_videos_json_filename = "videos.json"
$db_videos_json_src = ".\json\$db_videos_json_filename"
$db_categories_json_filename = "categories.json"
$db_categories_json_src = ".\json\$db_categories_json_filename"

Copy-Item -Force -Recurse $src -Destination $dst

docker compose build
docker compose up -d

sleep 10

docker cp $db_videos_json_src mongodb:/home/
docker cp $db_categories_json_src mongodb:/home/

docker exec mongodb mongoimport -u restheart -p R3ste4rt! --authenticationDatabase admin --db myflix --collection videos --drop --file /home/$db_videos_json_filename
docker exec mongodb mongoimport -u restheart -p R3ste4rt! --authenticationDatabase admin --db myflix --collection categories --drop --file /home/$db_categories_json_filename