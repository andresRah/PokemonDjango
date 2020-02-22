from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
# Create your views here.
post = [
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    },
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    },
    {
        'name': 'MontBlanc',
        'user': 'Andres Arevalo',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://d500.epimg.net/cincodias/imagenes/2019/08/14/motor/1565771492_166386_1565771651_noticia_normal.jpg'
    }
]

posts = [
    {
        'title': 'Mont Blanc',
        'user': {
            'name': 'Yésica Cortés',
            'picture': 'https://picsum.photos/60/60/?image=1027'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/600?image=1036',
    },
    {
        'title': 'Via Láctea',
        'user': {
            'name': 'Andres Leonardo Arevalo',
            'picture': 'https://picsum.photos/60/60/?image=1005'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/800/?image=903',
    },
    {
        'title': 'Nuevo auditorio',
        'user': {
            'name': 'Camilo Barrera',
            'picture': 'https://picsum.photos/60/60/?image=883'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/500/700/?image=1076',
    }
]

def list_pokemon(request):
    return render(request, 'feed.html', {'posts' : posts})

def list_pokemon1(request):
    """List existings pokemons"""
    content = []
    for p in post:
        content.append("""
             <p><strong>{name}</strong></p>
             <p><small>{user} - <i>{timestamp}</i></small></p>
             <figure><img src="{picture}"/></figure>
        """.format(**p))
    return HttpResponse('<br>'.join(content))
