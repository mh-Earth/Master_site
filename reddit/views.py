from django.shortcuts import render,HttpResponse,redirect
from .models import RedditAdmin,RedditAdminPlaneUrls,RedditPosted,RedditSettings,RedditSubmission
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import json,string,random,time
from .decorators import *
from .reddit import Reddit


reddit_api = Reddit()

@csrf_exempt 
def gen_random_string(lenght:int):
    char_lists = []
    char_lists.extend(string.ascii_letters + string.digits)
    random.shuffle(char_lists)
    password = ''.join(char_lists[0:lenght])
    return password

@validate_json_request
@require_api_key
@csrf_exempt 
def create_admin(request):
    if request.method == 'POST':
        """
        View to create a new admin user.
        """
        # Check if an admin user already exists using a more efficient method.
        if RedditAdmin.objects.exists():
            logging.info('{"Message":"Max user reached"}')
            return JsonResponse({"Message": "Max user reached"}, status=200)

        try:
            # Load the JSON data from the request body.
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            # Create and save a new Admin user in a single step.
            new_admin = RedditAdmin.objects.create(username=username, password=password)

            # Return a success message with the new admin's data.
            return JsonResponse({"username": new_admin.username, "password": new_admin.password}, status=200)

        except KeyError as e:
            # Catch a KeyError if the JSON payload is missing a key.
            logging.error(f"Keyword error: {e}")
            return JsonResponse({"Message": f"Invalid Data. Correction: {e}"}, status=400)

        except Exception as e:
            # Catch any other unexpected errors.
            logging.error(e)
            return HttpResponse("Server Error", status=500)
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 


@csrf_exempt 
def check_admin(request):
    if request.method == "GET":
        if RedditAdmin.objects.exists():
            return JsonResponse({"admin":True,"code":200},status=200,headers={"Access-Control-Allow-Origin": "*"})
        else:
            return JsonResponse({"admin":False,"code":200},status=200,headers={"Access-Control-Allow-Origin": "*"})
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 
            
@require_api_key
@require_password
@password_auth
@csrf_exempt 
def delete_admin(request):
    try:
        if request.method == 'DELETE':
            admin = RedditAdmin.objects.first()
            if not admin:
                return JsonResponse({"massage":"Admin not found"},status=200,headers={"Access-Control-Allow-Origin": "*"})
            admin.delete()
            return JsonResponse({"msg":"DELETED"},status=200,headers={"Access-Control-Allow-Origin": "*"})
        else:
            return JsonResponse({},status=405,headers={"Access-Control-Allow-Origin": "*"})

    except Exception as e:
        return JsonResponse(f"{e}",status=500,headers={"Access-Control-Allow-Origin": "*"})
        # return HttpResponse({})
        
@csrf_exempt 
def genarate_admin_url(request):
    # step 1: Genarate an url
    try:
        new_admin_url = RedditAdminPlaneUrls.objects.create(slug=gen_random_string(64),create_at=time.time(),live=600,expired=False)
        logging.info(new_admin_url)
        return JsonResponse(new_admin_url.to_json(),status=200)
    except Exception as e:
        logging.error(e)
        
@csrf_exempt         
def check_admin_url_slug_validation(slug:str) -> tuple[RedditAdminPlaneUrls,bool]:
    '''
    check if the genarate urls is still valid
    '''
    slug_row:RedditAdminPlaneUrls  = RedditAdminPlaneUrls.objects.filter(slug=slug).first()
    # if there is a slug the check the validation
    if slug_row:
        # if the time is expried then delete the slug from db
        time_gap:float = round(time.time() - slug_row.create_at,2)
        if time_gap > slug_row.live:
            return (slug_row,False)
        else:
            return (slug_row,True)
    else:
        return (slug_row,False)
    
# @csrf_exempt     
def isHasAdminUser() -> bool:
    '''
    check for admin user exsits
    '''
    return RedditAdmin.objects.exists()

@require_api_key
@csrf_exempt 
def adminpanel(request):
    if request.method == "POST":
        # step 1: Genarate an url
        jsondata = json.loads(request.body)
        print(jsondata)
        try:
            slug = jsondata['slug']
        except KeyError as e:
            logging.error(f"Keyword error {e}")
            return JsonResponse({"username":"","code":404})
        # check if the slug is valid or not
        validation = check_admin_url_slug_validation(slug)
        if validation[1]:
            admin = RedditAdmin.objects.first()
            if admin:
                logging.info('{"username":admin.username,"code":200}) , 200 , {"Access-Control-Allow-Origin": "*"}')
                return JsonResponse({"username":admin.username,"code":200}, status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
            logging.info('{"username":admin.username,"code":200}) , 200 , {"Access-Control-Allow-Origin": "*"}')
            return JsonResponse({"username":"","code":404} ,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
            
        else:
            try:
                RedditAdminPlaneUrls.objects.delete(validation[0])
            except Exception as e:
                pass
            
    logging.info('{"code":404}),404')
    return JsonResponse({"code":404},status=404)


# http://localhost:3000/get/meme/hot
@require_api_key
@csrf_exempt 
def getallsubs(request,sub_reddit:str,mode:str,limit:int=10):
    if request.method == "GET":
        valid_mode = ["new","hot","day","rising"]

        if mode not in valid_mode:
            return f"Invalid mode '{mode}'" ,404

        subs = reddit_api.submission_from_subreddit(subReddit=sub_reddit,mode=mode,limit=limit)
        previous_subs = RedditSubmission.objects.all()

        for sub in previous_subs:
            for index,new_sub in enumerate(subs['submission']):
                if sub.name == new_sub['name']:
                    subs['submission'].pop(index)
        subs.update({"total":len(subs['submission']),"hasAdmin":isHasAdminUser()})
        logging.debug(subs)
        return JsonResponse(subs)

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

@require_api_key
@require_password
@password_auth
@csrf_exempt 
def save(request,name:str=None):
    if request.method == 'POST':
            try:
                jsondata = json.loads(request.body)
                for sub in jsondata['submissions']:
                    RedditSubmission.objects.create(name=sub['name'],title=sub['title'])
                    
                return JsonResponse({}, status=200, headers={"Access-Control-Allow-Origin": "*"})
            except KeyError as e:
                logging.error('{"Message":f"Invaild Data. Correction:{e}"}')
                return JsonResponse({"Message":f"Invaild Data. Correction:{e}"})
            except Exception as e:
                logging.error(e)
                return JsonResponse({}, status=500, headers={"Access-Control-Allow-Origin": "*"})

      
    elif request.method == 'PUT':
        if request.body:
            jsondata = json.loads(request.body)
            submission:RedditSubmission = RedditSubmission.objects.filter(name=name).first()
            if submission:
                try:
                    submission.tags = jsondata['tags']
                    submission.title = jsondata['title']
                    submission.save()
                except KeyError as e:
                    logging.info('{"Message":f"Invaild Data. Correction:{e}"}')
                    return JsonResponse({"Message":f"Invaild Data. Correction:{e}"})
                except Exception as e:
                    logging.error(e)
                    return JsonResponse({}, status=500, headers={"Access-Control-Allow-Origin": "*"})
                logging.info(submission)
                return JsonResponse(submission,status=500, headers={"Access-Control-Allow-Origin": "*"})
            else:
                logging.info('{"Message":"Submission Not Found"}) ,404,{"Access-Control-Allow-Origin": "*"}')
                return JsonResponse({"Message":"Submission Not Found"}) ,404,{"Access-Control-Allow-Origin": "*"}

        else:
            data = {
                "error":"No submission data found"
            }
            logging.info(data)
            return JsonResponse(data,status=200)

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

@require_api_key
@csrf_exempt 
def getall(request):
    if request.method == "GET":
        all_submissions:list[RedditSubmission] = RedditSubmission.objects.all()
        name = [item.name for item in all_submissions]

        settings = RedditSettings.objects.first()
        if settings == None:
            settings = RedditSettings(limit=50,mode="day",is_reversed=True)


        if settings.is_reversed:
            all_submissions.reverse()
            name.reverse()

        # Getting all info about the submission from reddit's server
        data = reddit_api.nameToDetails(name)

        # merging OG data from reddit server and local data server data (tags,title etc...)
        for index,subs in enumerate(data["submission"]):
            subs.update({
                'tags':all_submissions[index].tags,
                'title':all_submissions[index].title,
                })
        
        data.update({"total":len(data['submission']),"hasAdmin":isHasAdminUser()})
        logging.debug(data)
        return JsonResponse(data,status=200)

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 


@csrf_exempt 
def show_all(request):
    if request.method == "GET":
        all_submissions = RedditSubmission.objects.all()
        all_names = [sub.name for sub in all_submissions]
        logging.info('{"names":all_names}) , 200 ,{"Access-Control-Allow-Origin": "*"}')
        return JsonResponse({"names":all_names},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

# http://localhost:3000/sub/id
# @bp.route("/api/show/<string:name>")
@require_api_key
@csrf_exempt 
def show(request,name:str):
    if request.method == "GET":
        submission = RedditSubmission.objects.filter(name = name).first()
        reddit_subs = reddit_api.submission(name.split("_")[1])
        

        # merge local and reddit server info
        data = {
            "name":reddit_subs.name,
            "id":reddit_subs.id,
            "title(OG)":reddit_subs.title, 
            "title":submission.title, # local
            "tags":submission.tags, # local
            "author":reddit_subs.author.name if reddit_subs.author != None else "Not found", #optional
            "score":reddit_subs.score if reddit_subs.score != None else "Not found", #optional
            "created_at":reddit_subs.created_utc if reddit_subs.created_utc != None else "Not found", #optional
            "upvote_ratio":reddit_subs.upvote_ratio if reddit_subs.upvote_ratio != None else "Not found", #optional
            "url":reddit_subs.url # most required
        }
        logging.info(JsonResponse(data))
        return JsonResponse(data,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
    
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 


#  http://localhost:3000/
@require_api_key
@require_password
@password_auth
@csrf_exempt 
def posted(request):
    if request.method == 'GET':
        all_posts = RedditPosted.objects.all()
        # logging.info('jsonify(all_posts) , 200 ,{"Access-Control-Allow-Origin": "*"}')
        all_posts = {"name":[post.name for post in all_posts]}
        print(all_posts)
        if all_posts:
            return JsonResponse(all_posts,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
        return JsonResponse({},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
    
    elif request.method == "POST":
        data = json.loads(request.body)
        res_json = {}
        for name in data['name']:
            if RedditPosted.objects.filter(name=name).first():
                res_json.update({name:'duplicated'})
            else:    
                RedditPosted.objects.create(name=name)
                res_json.update({name:'ok'})
        logging.info(JsonResponse(res_json))
        return JsonResponse(res_json,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
        
    elif request.method == "DELETE":
        jsondata = json.loads(request.body)
        res_json = {}
        try:
            for name in jsondata.get('name'):
                submission = RedditPosted.objects.filter(name=name)
                if submission:
                    submission.delete()
                    res_json.update({name:"ok"})
                else:
                    res_json.update({name:"failed"})

            logging.info(res_json)
            return JsonResponse(res_json,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
        except KeyError:
            logging.error("keyword error:{Message:Invaild Data}")
            return JsonResponse({"Message":"Invaild Data"})
        except Exception as e:
            logging.error(e)
            return "Server Error" , 500
            
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 



# @bp.route("/api/" , methods=['DELETE'])
@require_api_key
@require_password
@password_auth
@csrf_exempt 
def remove(request,name):
    if request.method == "DELETE":
        # delete from database
        submission = RedditSubmission.objects.filter(name=name).first()
        if submission:
            submission.delete()
        return JsonResponse({} ,status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
    
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

# DELETE ONE OR MANY SUBMISSIONS
@require_api_key
@require_password
@password_auth
@csrf_exempt 
def removes(request):
    if request.method == "DELETE":
        jsondata = json.loads(request.body)
        try:
            for name in jsondata.get('names'):
                submission = RedditSubmission.objects.filter(name=name).first()
                if submission:
                    submission.delete()
            return JsonResponse({"Message":f'Deleted:{jsondata['names']}'},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
            
        except KeyError:
            logging.error("keyword Error")
        except Exception as e:
            logging.error(e)
            return JsonResponse({"msg":"Server Error"},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

@require_api_key
@csrf_exempt 
def checkSubreddit(request,subreddit):
    if request.method == 'GET':
        is_exits =  reddit_api.check(subreddit)

        if is_exits:
            logging.info("status:200")
            return JsonResponse({},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 

        logging.info("status:404")
        return JsonResponse({},status=404 ,headers={"Access-Control-Allow-Origin": "*"}) 
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

# delete all submissions
@require_api_key
@require_password
@password_auth
@csrf_exempt 
def delete_all(request):
    if request.method == "DELETE":
        RedditSubmission.objects.all().delete()
        # Delete all entries in the model
        logging.info('"DELETED" ,200')
        return JsonResponse({},status=200 ,headers={"Access-Control-Allow-Origin": "*"}) 
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 
    
@csrf_exempt 
def home(request):
    if request.method == "DELETE":
        return JsonResponse({"status":"Running"},status=200)

    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 
        


@require_api_key
@csrf_exempt 
def settings(request):
    if request.method == 'POST':
        new_data = json.loads(request.body)
        settings_data = RedditSettings.objects.first()
        settings_data.limit = new_data["limit"]
        settings_data.mode = new_data["mode"]
        settings_data.is_reversed = new_data["is_reversed"]
        settings_data.save()
        logging.info(f"setting updated: {settings_data}")
        return JsonResponse({},status=200)

    elif request.method == 'GET':

        if len(RedditSettings.objects.all()) == 0:

            initial_settings = RedditSettings.objects.create(limit=50,mode="day",is_reversed=True)
            logging.info(initial_settings)
            return JsonResponse(initial_settings.to_json(),status=200)


        settings = RedditSettings.objects.first()
        
        logging.info(settings)
        return JsonResponse(settings.to_json(),status=200)
    
    else:
        return JsonResponse({},status=405 ,headers={"Access-Control-Allow-Origin": "*"}) 

