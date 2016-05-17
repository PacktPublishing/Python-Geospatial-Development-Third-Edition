from django.shortcuts import render

from hello.models import Counter

def say_hello(request):

    counter = Counter.objects.first()
    if counter == None:
        counter = Counter(count=0)

    counter.count = counter.count + 1
    counter.save()

    return render(request, "say_hello.html",
                  {'count' : counter.count})

