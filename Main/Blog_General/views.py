 


import os
from distutils import errors

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.detail import DetailView

from Blog_General.forms import BlogImagenForm, PublicacionForm
from Blog_General.models import BlogImagen, Comentario, Publicacion
from Main.settings import MEDIA_URL

from .forms import NewCommentForm, PublicacionFormAdmin

# Create your views here.

# Esta vista renderiza cada objeto de Publicacion en vistas separadas.
class PostDetalle(DetailView):
    model = Publicacion 
    context_object_name = 'post'
    template_name = 'GeneralPost.html'
    
    # Pasamos como contexto la clase comentarios para renderizar los mismos junto con los Likes.
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked= False

        comments_connected = Comentario.objects.filter(blogpost_connected= self.get_object()).order_by('-date_added')
        data['comments']= comments_connected
        stuff= get_object_or_404(Publicacion, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        data['total_likes']= total_likes
        

        
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked= True

        data["liked"]= liked    
       

    

        if self.request.user.is_authenticated:
            data['comment_form']= NewCommentForm(instance=self.request.user)
            
        return data

    def post(self, request, *args, **kwargs):
        new_comment= Comentario(body= request.POST.get('body'), 
            user= self.request.user,
            blogpost_connected= self.get_object())
        
        new_comment.save()
        return self.get(self, request, *args, **kwargs)



def NewPostSave(request): # Utilizamos esta funcion para guardar los datos obtenidos atravez de Post en la class Publicacion
    if request.method == 'POST': # Consultamos Method
        if request.user.is_authenticated: # Consultamos si esta logged
            
            ImgForm = BlogImagenForm(request.POST, request.FILES)
            
            #Obteniendo datos del registro (Form)
            titulo = request.POST['titulo']
            contenido = request.POST['contenido']
            user = User.objects.get(id=request.user.id)
            descripcion = request.POST['descripcion']
            
            #Guardando los datos en la DB
            publicacion = Publicacion(titulo=titulo, contenido=contenido, user=user, descripcion=descripcion)
            publicacion.save()
            print(publicacion.id)
            if ImgForm.is_valid():
                ImagenPost = ImgForm.cleaned_data
                print(ImagenPost)
                if ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=publicacion).last():
                    print("1")
                    imagenB = BlogImagen.objects.filter(publicacion_id=publicacion).last()
                    imagenB.save()
                elif ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=publicacion.id).last() == None:
                    print("2")
                    imagenB = BlogImagen(publicacion_id=publicacion, imagen=os.path.join(MEDIA_URL, 'img/defaultblog.jpg'))
                    imagenB.save()
                elif ImagenPost['imagen'] != None:
                    print("3")
                    print(ImagenPost["imagen"])
                    imagenB = BlogImagen(publicacion_id=publicacion, imagen=ImagenPost["imagen"])
                    imagenB.save()    
               
        return render(request, "indexBase.html", {"mensaje": "Gracias por Publicar, tu publicacion se encuentra en etapa de revision."})   
    else:            
        posteos = Publicacion.objects.filter(muestra_inferior="si").filter(publicado="publicado")
        return render(request, 'indexBase.html',{'posteos':posteos})


@login_required # Definimos que para poder postear es necesario estar conectado.
def NewPost(request):
    
    form = AuthenticationForm() 
    pform = PublicacionForm()
    ImgForm = BlogImagenForm()
    return render(request, 'makeanewpost.html', {'form': form, 'pform':pform,'ImgForm':ImgForm}) #Renderizamos mañeanewpost.


def blog_general_index(request): # Utilizamos esta def para establecer la paginacion segun la cantidad de objetos de Publicacion.
    try:
        listado_posts= Publicacion.objects.filter(publicado="publicado").order_by('-id') # Obtenemos los objetos
        paginator= Paginator(listado_posts, 6) # Determinamos la cantidad que queremos renderizar
        pagina= request.GET.get('page') or 1 
        posts= paginator.get_page(pagina)
        pagina_actual= int(pagina)
        paginas= range(1, posts.paginator.num_pages + 1) # Rango de paginas que se crearan.

        return render(request, 'Blog_Generalindex.html', {'posts': posts, 'pagina_actual': pagina_actual, 'paginas': paginas})
    except:
        return render(request, 'Blog_Generalindex.html') #Realizamos un except para que si no hay posts que renderizar no arroje error.

def darLike(request, pk): # Contabilizamos los likes , recibe la request y el id de la pagina.
    
    if request.user.is_authenticated: #Consultamos si esta logged
        post = Publicacion.objects.get(id=pk) 
        liked= False
        # post.likes.add(request.user)
        # post.save()#Guardamos los likes dentro de Publicacion
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked= True
            


        
    return HttpResponseRedirect(reverse('verpost', args=[str(pk)])) # Redireccionamos a el mismo blog


def eliminarPost(request, pk): #Eliminar posteo
    
    if request.method == 'POST':
    
        post = get_object_or_404(Publicacion, id=pk)
       
        if request.user == post.user: # Consultamos si el que intenta eliminar es el propietario del Post.
            post.delete() # Eliminamos el post 
            return HttpResponseRedirect(reverse('blog_general_index')) # Renderiza IndexBlog
        else:
            return render(request,'Blog_Generalindex.html') # Renderiza IndexBlog
    else:
        
        return render(request,'Blog_Generalindex.html') # Renderiza IndexBlog
    

@staff_member_required
def eliminarPostAdmin(request, pk): #Eliminar posteo
    
    if request.method == 'POST':
    
        post = get_object_or_404(Publicacion, id=pk)
        post.delete() # Eliminamos el post 
        return HttpResponseRedirect(reverse('blog_general_index')) # Renderiza IndexBlog        
    else:
        
        return render(request,'Blog_Generalindex.html') # Renderiza IndexBlog


def editPost(request, id): # Editar Posteo.

    post = Publicacion.objects.get(id=id) #Obtenemos el objeto segun id
    
    if request.method == 'POST':  #Si el method es POST remplazaremos los campos del Objet por los ingresados en la Request
        
        miPost = PublicacionForm(request.POST)
        
        if miPost.is_valid():

            post.__dict__.update(miPost.cleaned_data)
            post.save()
            

            if ImgForm.is_valid():
                ImagenPost = ImgForm.cleaned_data
                print(ImagenPost)
                if ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=post).last():
                    print("1")
                    imagenB = BlogImagen.objects.filter(publicacion_id=post).last()
                    imagenB.save()
                elif ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=post.id).last() == None:
                    print("2")
                    imagenB = BlogImagen(publicacion_id=post, imagen=os.path.join(MEDIA_URL, 'img/defaultblog.jpg'))
                    imagenB.save()
                elif ImagenPost['imagen'] != None:
                    print("3")
                    print(ImagenPost["imagen"])
                    imagenB = BlogImagen(publicacion_id=post, imagen=ImagenPost["imagen"])
                    imagenB.save()

            return render(request, "indexBase.html", {"mensaje": "Datos Actualizados tu publicacion se encuentra en etapa de revision."})
        else:
            context = miPost.errors# Volvemos al blog editado
            return render(request,'editarPosteoAdmin.html', {'miPost': miPost, 'post_id': id, 'titulo': post.titulo,'errors':context})   
    else: # De lo contrario pasamos los formularios correspondientes a editarPosteo.

        miPost = PublicacionFormAdmin(initial={'titulo': post.titulo, 'contenido': post.contenido, 'imagen': post.imagen, 'descripcion': post.descripcion})        
        ImgForm = BlogImagenForm()
        return render(request,'editarPosteoAdmin.html', {'miPost': miPost, 'post_id': id, 'titulo': post.titulo,'ImgForm':ImgForm})


def buscarPost(request): #Buscar Posteo
    if request.GET["titulo"]:

        titulo = request.GET["titulo"] #Obtenemos el titulo como parametro de busqueda.

        if titulo != None: #Si se ingreso informacion obtendra todos los objetos dentro de Publicacion que correspondan al titulo.

            publicacionBody = Publicacion.objects.filter(contenido__contains=titulo).filter(publicado="publicado")
            print(publicacionBody)
            if len(publicacionBody) == 0: # Consultamos si se escribio algo en el form.
                
                return HttpResponseRedirect(reverse('blog_general_index')) # Lo devolvemos al IndexBlog
            else:
                # Si hay resultados renderizamos los objetos obtenidos.
                return render(request, 'Blog_Generalindex.html', {'buesqueda_posteos': publicacionBody})
        else:
            # Si no se busco nada se vuelve a IndexBlog.
            return HttpResponseRedirect(reverse('blog_general_index'))

    else: # Si es POST renderizamos IndexBlog.
        return HttpResponseRedirect(reverse('blog_general_index'))


@staff_member_required
def adminPosts(request):
    draft = Publicacion.objects.filter(publicado="draft")
    publicados = Publicacion.objects.filter(publicado="publicado")
    
    return render(request, 'adminPost.html', {'drafts':draft,'publicados':publicados})


@staff_member_required
def editPostAdmin(request, id): # Editar Posteo.

    post = Publicacion.objects.get(id=id) #Obtenemos el objeto segun id
    
    if request.method == 'POST':  #Si el method es POST remplazaremos los campos del Form por los ingresados en la Request
        
        miPost = PublicacionFormAdmin(request.POST)
        ImgForm = BlogImagenForm(request.POST, request.FILES)

        if miPost.is_valid():

            post.__dict__.update(miPost.cleaned_data)
            post.save()
             

            if ImgForm.is_valid():
                ImagenPost = ImgForm.cleaned_data
                print(ImagenPost)
                if ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=post).last():
                    print("1")
                    imagenB = BlogImagen.objects.filter(publicacion_id=post).last()
                    imagenB.save()
                elif ImagenPost['imagen'] == None and BlogImagen.objects.filter(publicacion_id=post.id).last() == None:
                    print("2")
                    imagenB = BlogImagen(publicacion_id=post, imagen=os.path.join(MEDIA_URL, 'img/defaultblog.jpg'))
                    imagenB.save()
                elif ImagenPost['imagen'] != None:
                    print("3")
                    print(ImagenPost["imagen"])
                    imagenB = BlogImagen(publicacion_id=post, imagen=ImagenPost["imagen"])
                    imagenB.save()   
               
            return render(request, "indexBase.html", {"mensaje": "Datos Actualizados tu publicacion se encuentra en etapa de revision."})
        else:
            context = miPost.errors# Volvemos al blog editado
            
            return render(request,'editarPosteoAdmin.html', {'miPost': miPost, 'post_id': id, 'titulo': post.titulo,'errors':context})   
    else: # De lo contrario pasamos los formularios correspondientes a editarPosteo.

        miPost = PublicacionFormAdmin(initial={'titulo': post.titulo, 'contenido': post.contenido, 'imagen': post.imagen, 'descripcion': post.descripcion})        
        ImgForm = BlogImagenForm()
        return render(request,'editarPosteoAdmin.html', {'miPost': miPost, 'post_id': id, 'titulo': post.titulo,'ImgForm':ImgForm})

            
            
            
    

     