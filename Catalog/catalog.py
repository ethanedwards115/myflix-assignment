import argparse
from sys import argv
import requests
import json
from flask import Flask, request, render_template

# Custom modules
import utils.logger as log

VIDEO_SERVER = "127.0.0.1"
DATABASE_SERVER = "127.0.0.1"

parser = argparse.ArgumentParser(description="Flask server for running the catalog service")
parser.add_argument("-d", "--debug", action="store_true",
                    required=False, help="Enables debug mode")
parser.add_argument("-s", "--video-server",
                    required=True, help="IP address or URL of associated video server")
parser.add_argument("-b", "--database",
                    required=True, help="IP address or URL of associated database")

app = Flask(__name__, static_folder='css')
app.debug = True

def fetch_success(tag: str):
    log.SUCCESS(f"[{tag}] :: fetch successful")

def check_response_for_error(response: requests.Response) -> str:
    if (response.status_code != 200):
        error = f"Unexpected response: {response.reason}. Status: {response.status_code}. Message: {response.json()['Exception']['Message']}"
        log.ERROR(error)
        return log.ERROR_STR(error)
    else:
        fetch_success(response.url)
        return ''

def make_html_list(item_list: list, href_context: str = './') -> str:

    html_list = ""

    for item in item_list:
        html_list += '<li><a class=\"dropdown-item\" href=\"' + href_context + str(item) + '\">' + str(item).capitalize() + '</a></li>\n'

    return html_list

def make_card(title: str, href: str, thumbnail_src: str) -> str:
    element = f"<div class=\"col-sm-12 col-md-12 col-lg-4 col-xl-3 d-flex mt-5 mb-1 justify-content-center\"> \
        <div class=\"card\"> \
            <a href=\"/Videos/{href}\"> \
                <img src=\"{thumbnail_src}\" class=\"card-img-top\" alt=\"{title}\"> \
            </a> \
        <div class=\"card-body\"><h5 class=\"card-title\">{title}</h5></div></div></div>"
    return element

@app.route('/')
def index_page():
    
    # Get list of categories
    response = requests.get(DATABASE_SERVER + "/myflix/categories")

    category_fetch_error = check_response_for_error(response)
    if category_fetch_error != '':
        return category_fetch_error
    
    json_categories = response.json()
    categories = [item['category'] for item in json_categories]
    
    # Get list of videos
    response = requests.get(DATABASE_SERVER + "/myflix/videos/")

    video_fetch_error = check_response_for_error(response)
    if video_fetch_error != '':
        return video_fetch_error
    
    json_videos = response.json()
    videos = [item['video'] for item in json_videos]

    html_list = make_html_list(categories, href_context='./Category/')
    
    card = ""
    for video in videos:        
        log.TRACE(video['Name'])
        card += make_card(video['Name'], video['uuid'], f"{VIDEO_SERVER}/pics/{video['thumb']}") + '\n'
    
    return render_template('index.html', categories=html_list, video_cards=card)



@app.route('/Videos/<uuid>')
def video_page(uuid):
    log.MESSAGE('['+request.remote_addr+'] --> ' + uuid)
    
    URL_UUID_FILTER = DATABASE_SERVER + '/myflix/videos?filter={"video.uuid":"' +uuid+ '"}'
    response = requests.get(URL_UUID_FILTER) 

    json_video = response.json()
    video = json_video[0]['video']

    video_error = check_response_for_error(response)
    if video_error != '':
        return video_error
        
    # .replace(':80', ':1935').replace('http://', 'rtmp://')
    src = VIDEO_SERVER + '/mp4/' +  video['file']
    
    return render_template("video.html", video_name=video['Name'], thumbnail=video['thumb'], poster=VIDEO_SERVER+'/pics/'+video['pic'], video_src=src)

@app.route('/Category/<category>')
def category_page(category):
    
    # Fetch all video data of this <category>
    response = requests.get(DATABASE_SERVER + '/myflix/videos?filter={"video.category":"'+category+'"}')
    
    videos_error = check_response_for_error(response)
    if videos_error != '':
        return videos_error

    json_videos = response.json()
    videos = [item['video'] for item in json_videos]
    
    # Get list of categories
    response = requests.get(DATABASE_SERVER + "/myflix/categories")  

    categories_error = check_response_for_error(response)
    if categories_error != '':
        return categories_error

    json_categories = response.json()
    categories = [item['category'] for item in json_categories]
    
    # Display all video data of this <category>
    html_list = make_html_list(categories)
    
    card = ""
    for video in videos:
        card += make_card(video['Name'], video['uuid'], f"{VIDEO_SERVER}/pics/{video['thumb']}") + '\n'
    
    return render_template('category.html', category=category, category_name=str(category).capitalize(), categories=html_list, video_cards=card)

@app.route('/Test/')
def hello_page():   
    response = requests.get(DATABASE_SERVER + "/myflix/videos")
    print(response)
    JSON_VIDEOS = response.json()
    VIDEOS = [item['video']['Name'] for item in JSON_VIDEOS]
    
    html_list = ""
    for item in VIDEOS:
        html_list += "<li>" +str(item).capitalize()+ "</li>\n"
        
    return render_template('index.html', items=list)

if __name__ == '__main__':

    print(argv)

    args = parser.parse_args()
    VIDEO_SERVER = args.video_server
    DATABASE_SERVER = args.database
    print(args)
    print(args.video_server)
    print(args.database)

    app.run(host='0.0.0.0', port=5000)