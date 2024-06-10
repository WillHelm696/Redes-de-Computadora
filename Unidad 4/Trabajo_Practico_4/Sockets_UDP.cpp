#include <iostream>
#include<fstream>
#include<string>

#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <arpa/inet.h>

using namespace std;

int main(){
    string nombreUsuario ;
    cout<< "Ingese Nombre de usuario";
    cin >> nombreUsuario;

    // Crear el socket UDP
    int socket_servidor = socket(AF_INET, SOCK_DGRAM, 0);
    if(socket_servidor<0){
        cout<<"\n Error creando socket";
        exit(1);
    }

    close(socket_servidor);

}