import os
import subprocess
import re

# Path donde se guardarán los archivos (Cambiar si el path a la carpeta donde se almacenan los archivos cambia)
path = 'C:/Users/martosad/OneDrive - Boehringer Ingelheim/Documentos/01_TASKS/Server_To_SNETS/'

def obtain_ips(servers):
    ips = []
    for server in servers:
        try:
            result = subprocess.run(['ping', '-n', '1', server], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            out = result.stdout
            start = out.find('[') + 1
            end = out.find(']', start)
            ip = out[start:end].strip()
            ips.append(ip)
        except Exception as e:
            continue  # Ignorar cualquier error y continuar con el siguiente servidor
    return ips

def create_folder(task):
    try:
        folder_path = os.path.join(path, task)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{task}' created successfully.")
        return folder_path
    except OSError as error:
        print(f"Error creating folder: {error}")
        return None

def main():
    # Solicitar inputs
    print("*********************")
    print("SERVER ON SNET to SNET")
    print("*********************")
    print("Introduce all the necessary information to create the file.")
    
    task = input("Task: ")
    caller = input("Caller ID: ")
    firewall = input("Firewall: ")
    servers = input("Server(s) (separated with '/'): ").split(' / ')
    new_ips = input("New IP(s) (separated with '/'): ").split(' / ')
    new_snet = input("New SNET: ")

    # Obtener la IP del servidor
    old_ips = obtain_ips(servers)
    old_ips_str = " / ".join(old_ips)
    servers_str = " / ".join(servers)
    new_ips_str = " / ".join(new_ips)
    b = r"/b"

    site = new_snet[4:7]
    snet_number = re.search(r'\d+', new_snet).group()

    # Convertir el Caller ID a mayúsculas
    if(caller.islower):
        caller = caller.upper()

    # Crear el contenido del archivo
    content = f"""*********************
SERVER ON SNET to SNET
*********************
Task: {task}
Change:
Caller ID: {caller}
FW: {firewall}
Server(s): {servers_str}
Old IP(s): {old_ips_str}
New IP(s): {new_ips_str}
MAC(s): 
Old SNET (If required): 
New SNET: {new_snet}

Affected Devices:



*********************
LAN CHECKS
*********************

---------------------
SWITCH
---------------------


---------------------
IMPLEMENTATION
---------------------



**************************
SERVER TO SNET FW
**************************
RDP Rule: 
	Group: 
		Add (The objects should be created with the NEW IP address for the SNET):
	- Name: {new_snet}_[RULE_NUMBER]
	- TAGS: {new_snet} BI_SNR7.7_RDP_TO_SNET
	- Source: 
		Zone:
			biprod
		Address:
			GR_ALL_BINET
		User:
			eu{b}i-is-firewalls-d{new_snet}a
	- Destination:
		Zone:
			snets
		Address:
			GR_{site}_{snet_number}-I-[RULE_NUMBER]
                {" / ".join([f'HO_{server}' for server in servers])}
                {" / ".join([f'{ip}/32' for ip in new_ips])}
	- Application:
		BI_AGRP_RDP
	- Service: 
		application-default
	- Description:
		#SNOW#{task}#
		#RO#{caller}#
			
Check if the SNET is added in to:
	GR_{site}_YY_SNR115_SOURCES 
	GR_{site}_YY_COMMVAULT_SOURCES  
	GR_{site}_YY_SNR4_SOURCES 
	GR_{site}_YY_SNR3.2_SOURCES 
"""

    # Guardar el contenido en un archivo TXT
    task_name = f"{task}.txt"
    folder_path = create_folder(task)
    if folder_path:
        file_path = os.path.join(folder_path, task_name)
        try:
            with open(file_path, "w") as file:
                file.write(content)
            print(f"File '{task_name}' created successfully.")
        except Exception as e:
            print(f"Error creating file: {e}")
    else:
        print("Failed to create folder, file not saved.")

if __name__ == "__main__":
    main()
