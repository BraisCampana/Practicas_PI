# classroom_PI
 
Cuenta de Twitter de la app: @spoti_FIC

Nombre Proyecto: SpotiFIC
----------------

Breve descripción de la aplicación, y un listado de las funcionalidades más relevantes:
  
  Aplicación Web enfocada a la búsqueda de canciones, artistas y álbumes usando las APIs de Spotify, Wikipedia y Twitter.
  
  * Caso de uso 1 :
    Login del usuario. El usuario introduce dos palabras clave (el nombre de la cuenta y su token) en los campos correspondientes. Una vez cubiertos, el usuario clica en el botón de “Iniciar sesión”.

  * Caso de uso 2 :
    Cambiar la categoría de búsqueda. El usuario hace click en el desplegable para poder seleccionar el filtro por el que hacer su búsqueda. Al seleccionar una opción del desplegable, el estado y el filtro de búsqueda cambiarán.

  * Caso de uso 3 :
    Búsqueda de canciones. El usuario introduce una palabra clave (nombre de la canción) en la barra de búsqueda. Al buscar, se muestra una lista de canciones que contienen parcialmente o en su totalidad la palabra clave.

  * Caso de uso 4 :
    Búsqueda de artista. El usuario introduce una palabra clave (nombre del artista) en la barra de búsqueda. Al buscar, se muestra una lista de artistas que contienen la palabra clave.

  * Caso de uso 5 :
    Búsqueda de álbum. El usuario introduce una palabra clave (nombre del álbum) en la barra de búsqueda. Al buscar, se muestra una lista de álbumes que contienen la palabra clave.

  * Caso de uso 6 :
    Ver detalles de canción. El usuario hace click en la canción de la que quiere obtener información. Se muestra un conjunto de información sobre la canción.

  * Caso de uso 7 :
    Ver detalles de artista. El usuario hace click en el artista del que quiera obtener información. Se muestra un conjunto de información sobre el artista.

  * Caso de uso 8 :
    Ver detalles de álbum. El usuario hace click en el álbum del que quiera ver sus canciones. Se muestra un conjunto de información del álbum junto con el listado de canciones y artistas que lo componen.

  * Caso de uso 9 :
    Ver detalles del usuario. El usuario hace click en su nombre de usuario en la parte superior derecha. La primera vez se redirige al usuario a una página para poder logearse en su cuenta de Spotify y pedirle permisos. Una vez logeado, cuando haga click en su usuario se muestra un conjunto de información, tanto de Twitter como de Spotify.
  
Integrantes Grupo:
------------------

  * Brais Campaña Martínez <brais.campana@udc.es>
  * Víctor Villar Vázquez <victor.villar@udc.es> 
  * Anxo Freire Balea <anxo.freire@udc.es>
  
Cómo ejecutar:
--------------

Secuencia de comandos (docker) para descargar y lanzar la aplicación:

  1.- En la carpeta donde queremos alojar el proyecto: git clone https://github.com/GEI-PI-614G010492122/aplicacion_django-campana_freire_villar.git

  2.- En VisualStudioCode pulsar en el menú de arriba: Archivo -> Abrir Carpeta... -> seleccionar la carpeta ../aplicacion_django-campana_freire_villar/spotific

  3.- Cuando cargue el proyecto, poner en el teclado la combinación "Ctrl+P" -> Poner ">" -> Pulsar en la opción "Remote-Containers: Rebuild and Reopen in Container"
  
  4.- Una vez cargado el workspace, poner en el terminal "cd /spotific" -> "python manage.py makemigrations" -> "python manage.py migrate" -> (en caso de querer crear un superusuario) "python manage.py createsuperuser"

  5.- La aplicación web se puede ejecutar de dos formas:

    5.a.- Acceder a la opción de "Ejecución y Depuración" dentro del menú lateral de VS (Ctrl+Mayus+D) -> Pulsar el triángulo verde con la opción "Python: Django"

    5.b.- Poner en el terminal dentro de la carpeta "/workspace/spotific": "python manage.py runserver 0.0.0.0:8080"

Problemas conocidos:
--------------------

  * Cuando un nuevo usuario es redireccionado a iniciar sesión en su cuenta de Spotify y cierra la ventana sin haberla iniciado, al intentar abrir esta página de nuevo no puede ya que el puerto está ocupado
  
Cambios con respecto al anteproyecto:
-------------------------------------

  * Registro de usuario: No implementamos los botones para linkear las cuentas de Twitter y Spotify. También añadimos a este apartado el campo de email y el campo de repetir contraseña.
  * Detalles de cancion: No mostramos la foto de la canción ya que la API de Spotify no nos la devuelve.
  * La cuenta de Twitter que se usa es una propia de la aplicación (@spoti_FIC).
