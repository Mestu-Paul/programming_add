from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Problem
from .models import Tag
import json

def problems(request):
    if request.method=="POST":
        pass
    else:
        # print("----------- now get request ---------- ")
        allProblems = Problem.objects.all()
        context = {'problems':[]}
        for p in allProblems:
            problem = {'name':p.name,'link':p.link,
                    'tags':[],'comment':p.comment,
                    'oj':p.judge, 'contributor':p.user}
            for t in p.tags.all():
                problem['tags'].append(t.name)
            context['problems'].append(problem)
        # print("context-----------\n",context)
        return render(request, 'problems.html',context=context)
    
@login_required
def addproblem(request):
    if request.method=="POST":
        problem_name = request.POST.get('problemName')
        problem_link = request.POST.get('problemLink')
        problem_judge = request.POST.get('judge')
        problem_tags = json.loads(request.POST.get('searchTags'))
        comment = request.POST.get('comment')
        user = request.user
        
        # print(problem_name)
        # print(problem_link)
        # print(problem_judge)
        # print(problem_tags)
        # print(comment)
        # print("user :",user)
        
        # Create a new problem object
        problem = Problem(name=problem_name, link=problem_link,judge=problem_judge, comment=comment, user=user)
        problem.save()

        # Add tags to the problem object
        for tag_name in problem_tags:
            # print("tag_name",tag_name)
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            problem.tags.add(tag)
            
    return render(request,'add_problems.html')

def filterProblem(request):
    if request.method=="POST":
        search_option = request.POST.get("searchOption")
        search_text = request.POST.get("searchText")
        # Filter the data based on the search option and search text
        if search_option == "tag":
            filtered_problems = Problem.objects.filter(tags__name__icontains=search_text)
        elif search_option == "judge":
            filtered_problems = Problem.objects.filter(judge__icontains=search_text)
        # Create a list of dictionaries for the filtered problems
        problems = []
        for p in filtered_problems:
            problem = {'name': p.name, 'link': p.link, 'tags': [], 'comment': p.comment,
                       'oj': p.judge, 'contributor': p.user}
            for t in p.tags.all():
                problem['tags'].append(t.name)
            problems.append(problem)
        # Render the template with the filtered data
        return render(request, "problems.html", {"problems": problems})
    
    return redirect('problems')


def searchSuggestion(request):
    search_option = request.GET.get('searchOption', '')
    search_text = request.GET.get('searchText', '')
    print('search option',search_option)
    print('search text',search_text)
    
    results = []
    if search_option == "tag":
        if search_text:
            tags = Tag.objects.filter(name__icontains=search_text)
            results = [tag.name for tag in tags]
            print("result",results)     
            pass
        else:
            tags = Tag.objects.all()
            results = [tag.name for tag in tags]
            print("result",results)
            pass
    elif search_option == "judge":
        if search_text:
            problems = Problem.objects.filter(judge__icontains=search_text,judge__startswith=search_text)
            results = [problem.judge for problem in problems]
            print("result",results)     
        else:
            problems = Problem.objects.all()
            results = [problem.judge for problem in problems]
            pass
    return JsonResponse(results, safe=False)