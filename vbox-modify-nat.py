#!/usr/bin/python
'''
Utiliza comandos de VBoxManage para relevar NICs en estado "bridge" y las modifica a estado "nat".
Soporta varias imagenes con multiples nics cada una. Setea TODAS en modo NAT.

Falta agragarle gestion de errores. 


'''

import os

comando_running = "VBoxManage list runningvms"
showvminfo = "VBoxManage showvminfo "
controlvm = "VBoxManage controlvm " #The controlvm subcommand allows you to change the state of a virtual machine that is currently running. 

resultado_running = os.popen(comando_running)
imagenes = {}

def relevo_imagenes():
    for line in resultado_running.readlines():
        salida_imagenes = line.split("{")
        imagenes[salida_imagenes[1].split("}")[0]] = salida_imagenes[0]

def relevo_bridge():
    activas = imagenes.keys()
#    print "NICs Activas"
    for activa in activas:
#       print "\nUUID: "+activa+" Imagen: "+imagenes[activa]
       comando_interface = showvminfo+activa+" --machinereadable"
       resultado_nics= os.popen(comando_interface)       
       for line in resultado_nics.readlines():
          if "nic" in line:
              if "bridged" in line:                
#                   print line.split("=")[0]
                   set_nat(activa, line.split("=")[0])

def set_nat(uuid, nic): 
       comando_nat = controlvm+uuid+" "+nic+" nat" 
       resultado_nat = os.popen(comando_nat)

relevo_imagenes()
relevo_bridge()
#print "\nCompruebo NICs sin Bridged"
#relevo_bridge()

