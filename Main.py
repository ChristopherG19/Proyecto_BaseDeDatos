'''
  Universidad del Valle de Guatemala
  Bases de datos 1
  Proyecto 2

  Integrantes:
    - Gabriel Vicente 20498
    - Maria Isabel Solano 20504
    - Christopher García 20541
'''

#Import de diferentes librerías y otros archivos .py
from Funciones import *
from ConnectionBD import *
from Admins import *
from Users import *
from datetime import datetime

Salir = False
opcion = 0

#Impresión menú principal y toma de decisión
while not Salir:
  escritura_lenta("\n\t\t\t\tMenu\n")
  escritura_lenta("1) Crear cuenta")
  escritura_lenta("2) Ingresar")
  escritura_lenta("3) Ingresar como Admin")
  escritura_lenta("4) Salir")
  print()

  opcion = SolicitudNum()

  #Opcion para crear cuenta
  if (opcion == 1):
    print()
    Verificador = False
    Correo = ""
    Contra = ""
    TipoCuenta = ""
    
    #Se verifica si los datos son válidos y se procede a crear la cuenta
    while not Verificador:
      Correo, Contra, TipoCuenta = CrearCuenta()
      if (Correo != None and Contra != None and TipoCuenta != None and Get_Cuenta(Correo) == None):
        CodigoP = GenerarCodigo('perfiles')
        print()
        #Se registra la fecha y hora en que se crea la cuenta
        Fecha = datetime.date(datetime.now())
        Hora = datetime.time(datetime.now())
        Daton = input("Nombre del perfil inicial: ")
        Upload_Cuenta(Correo, Contra, TipoCuenta, Fecha, Hora)
        Upload_Perfiles(CodigoP, 1, Daton)
        Upload_CuentaPerfiles(Correo, CodigoP)
        escritura_lenta("\n\t\t\tCuenta registrada exitosamente\n")
        Verificador = True  
      else:
        print("\nAlgo salio mal, intente nuevamente\n")
  
  #Opcion para ingresar
  elif (opcion == 2):
    verificador_menu = False
    Verificador = False
    Correo = ""
    Contra = ""
    PerfilActual = ""
    Contador = 0
    #Se verifica si la cuenta está en la base de datos 
    #De estarlo se le permite al usuario ingresar y utilizar las opciones disponibles
    #De no ingresar correctamente se cuentan los intentos fallidos
    while not Verificador:
      Correo, Contra = LoginCuenta() 
      if(LogIn(Correo, Contra) != None and LogIn(Correo, Contra) == True):
        escritura_lenta("Ingreso exitoso\n")
        ManejoPerfiles(Correo)
        PerfilActual = Get_PerfilIn(Correo)
        Verificador = True
      elif(LogIn(Correo, Contra) == False):
        print("Cuenta desactivada, pruebe con otra\n")
      else:
        contadorC = getContador(Correo)
        Fecha = datetime.now()
        if (Get_Cuenta(Correo) != None and contadorC == None):
          Contador += 1
          Upload_Intentos(Correo, Fecha, 1)
        elif (Get_Cuenta(Correo) != None and contadorC != None):
          contadorC += 1
          UpdateIntentos(contadorC, Fecha, Correo)
        else:
          print("Error, correo o contraseña incorrecta\n")
    
    #Luego de ingresar correctamente el usuario puede usar todas las funciones
    while not verificador_menu:
      print("\n________________________________________\n")
      escritura_lenta("\tPerfil activo: "+ PerfilActual)
      print("\n________________________________________\n")
      print("Elija la accion a realizar\n")
      print("1) Mostrar recomendaciones")
      print("2) Mostrar películas")
      print("3) Mostrar favoritos")
      print("4) Mostrar peliculas sin terminar")
      print("5) Mostrar peliculas vistas")
      print("6) Busqueda personalizada")
      print("7) Cambiar Perfil")
      print("8) Cerrar Sesion")
      print()

      seleccion = SolicitudNum()

      #Se procede a determinar que procede en base a la opcion seleccionada
      if (seleccion==1):
        escritura_lenta("Mostrando recomendaciones\n")
        recomendaciones(Get_CodigoPerfil(Correo, PerfilActual))
        
      elif (seleccion==2):
        escritura_lenta("Mostrando películas\n")
        ver_peliculas(Correo, PerfilActual)

      elif (seleccion==3):
        escritura_lenta("Mostrando favoritos\n")
        mostrarfavoritos(Get_CodigoPerfil(Correo, PerfilActual))

      elif (seleccion==4):
        escritura_lenta("Mostrar peliculas sin terminar\n")
        mostrarviendo(Get_CodigoPerfil(Correo, PerfilActual))

      elif (seleccion==5):
        escritura_lenta("Mostrar peliculas vistas\n")
        mostrarvistos(Get_CodigoPerfil(Correo, PerfilActual))

      elif (seleccion==6):
        escritura_lenta("Busqueda personalizada\n")
        SearchP()

      elif (seleccion==7):
        if (Get_Sub(Correo) == "Gratis"):
          print("\nLo sentimos, no puedes cambiar de perfil")
          print("El tipo de cuenta no lo permite")
        else:
          PerfilActual = CambioPerfiles(Correo, PerfilActual)
        
      elif (seleccion==8):
        escritura_lenta("Cerrar Sesion\n")
        verificador_menu = True
    
  #Opcion para ingresar como Administrador
  elif (opcion == 3):
    print()
    menu_admin_L1 = True
    while (menu_admin_L1):
      #ingreso de sesión
      verificador = True
      usuario = input('Usuario: ')
      contra = getpass('Contraseña: ')
      #Se encripta la contraseña
      md5_hash = hashlib.md5()
      md5_hash.update(contra.encode())
      contra = md5_hash.hexdigest()
      #Se verifica que el usuario administrador esté en la base de datos y luego se le permita entrar
      while (verificador):
        if(LogInAdmin(usuario, contra) != None):
          Nombre = LogInAdmin(usuario,contra)
          print('Ingreso exitoso, bienvenido/a ', Nombre) 
          print('Pulse enter para continuar\n')
          confirmation = input()

          #inicio del ciclo while para mostrar opciones
          menu_admin_L2 = True
          while (menu_admin_L2):          
            #impresión de opciones
            print('\nIngrese el número de la opción que desea realizar:')
            print('__________________________________________________________')
            print('\n1) Agregar contenido')
            print('2) Modificar contenido')
            print('3) Eliminar contenido')
            print('\n4) Modificar usuarios')
            print('5) Desactivar/Activar usuarios')
            print('\n6) Agregar anunciantes')
            print('7) Modificar anunciantes')
            print('8) Eliminar anunciantes')
            print('\n9) Agregar anuncios')
            print('10) Modificar anuncios')
            print('11) Eliminar anuncios')
            print('12) Reportes')
            print('\n13) Cerrar sesión')
            print('__________________________________________________________')
            print()

            op1 = input("Opcion: ")

            #Se procede a determinar que procede en base a la opcion seleccionada

            if (op1 == '1'):
              #Agregar contenido
              AgregarContenido()

            elif (op1 == '2'):
              #Modificar contenido
              ModContenido_pelicula()

            elif (op1 == '3'):
              #Eliminar contenido
              Eliminar_pelicula()

            elif (op1 == '4'):
              #Modificar usuario
              Modifi_Usuarios()
                        
            elif (op1 == '5'):
              #Desactivar usuario
              desactivar_Usuarios()

            elif (op1 == '6'):
              #Agregar anunciantes
              Agregar_Anunciantes()

            elif (op1 == '7'):
              #Modificar anunciantes
              ModAnunciantes()
                
            elif (op1 == '8'):
              #Eliminar anunciantes
              EliminarAnunciantes()

            elif (op1 == '9'):
              #Agregar anuncios
              Agregar_Anuncios()

            elif (op1 == '10'):
              #Modificar Anuncios
              ModAnuncios()

            elif (op1 == '11'):
              #Eliminar anunciantes
              EliminarAnuncios()

            elif (op1 == '12'):
              #Agregue esto
              ver1 = True
              while (ver1):
                print('\n-------------------- Reportes --------------------')
                print('Ingrese el número de la opción que desea realizar:')
                print('__________________________________________________________')
                print('1) Top 10 generos mas vistos y minutos consumidos')
                print('2) Cantidad de reproducciones por genero y tipo de cuenta')
                print('3) Top 10 actores y directores de peliculas mas vistas por cuentas estandar y avanzadas')
                print('4) Cantidad cuentas avanzadas creadas en los últimos 6 meses')
                print('5) Hora pico del servicio')
                print('6) Anuncios vistos por cuentas gratis')
                print('7) Salir') 
                print('__________________________________________________________\n')
                op12 = SolicitudNum2()

                if op12 == 1:
                  reporte_1()
                elif op12 == 2:
                  reporte_2()
                elif op12 == 3:
                  reporte_3()
                elif op12 == 4:
                  query_reporte_4()
                elif op12 == 5:
                  reporte_5()
                elif op12 == 6:
                  query_reporte_6()
                elif op12 == 7:
                  ver1 = False
    
            elif (op1 == '13'):
              #Cerrar sesión
              usuario = ""
              contra = ""
              menu_admin_L1 = False
              verificador = False
              menu_admin_L2 = False

        #Si el usuario administrador no se registra correctamente se le indica si quiere seguir intentando
        else:
          print()
          escritura_lenta("Usuario o contraseña incorrecta")
          escritura_lenta('Desea probar nuevamente? ')
          op = input('(y/n): ')
          if (op == 'n'):
            menu_admin_L1 = False
            verificador = False
          else:
            verificador = False
  
  elif (opcion == 4):
    Salir = True
    
  else:
    print("Opcion invalida")
    
  #Se termina el programa