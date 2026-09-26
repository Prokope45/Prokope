"""Blog views.

Author: Jared Paubel
Version: 0.1
"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# GitHub-to-PythonAnywhere Update Webhook
@csrf_exempt
def update(request):
    """Update webook. Dead code."""
    if request.method == "POST":
        '''
        Pass the path of the directory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        '''
        # NOTE: dead code pending removal -- `Repo` is never imported, so a POST
        # to /blog/update_server/ would raise NameError. See the issue tracked
        # for deleting this view and its URL entry.
        repo = Repo("django-tech-blog")  # noqa: F821

        git = repo.git
        git.checkout('master')

        git.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse(
            "Couldn't update the code on PythonAnywhere",
        status=400)
