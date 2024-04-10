#include<iostream>
#include<fstream>
#include<string>

using namespace std;

void analizar_tramas(string tramas){
    int tramas_totales = 0 ;
    int tramas_longitud_correcta = 0 ;
    int tramas_longitud_incorrecta = 0;
    int tramas_checksum_correcto = 0 ;
    int tramas_checksum_incorrecto = 0 ;
    int tramas_secuencia_escape = 0 ;
    int i = 0 ;

    while (i <= tramas.length()){
        bool flag = false;  // Flag verificara si se encontro una secuencia de escape
        bool escape = false; //escape Verificara si la longitud esta incorecta
        int suma = 0 ; // Suma calculara el checksun de la trama

        string byte_bandera = tramas.substr(i,2);
        if (byte_bandera == "7E"){
            string byte_longitud = tramas.substr(i+2,4); // Toma los 2 byte para la longitud
            string sub_trama ; // Sub_Trama Seleciona se encadena las tramas despues de la longitud

            int longitud = stoi(byte_longitud, nullptr, 16); // Convierte la el byte longitud a base 10 
            int j = i+6; // Inicia en la trama despues de calcular la longitud  
            while ( j < ( i + 6 + longitud * 2 ) ){ 
                string byte = tramas.substr(j,2); // Extrae byt a byt de la trama
                if (byte == "7E"){
                    string byte_escape = tramas.substr(j-2,2); // Si se encontro un Byte 7E verifica si antes hay un 7D
                    if (byte_escape != "7D"){ 
                        escape = true; // EN caso de no haber un 7D se activa el escape y se toma como longitud incorecto
                        //i += 2; 
                        break;
                    }
                    tramas_secuencia_escape ++ ; // En caso de encontrar un 7D se suma a la secuencia de escape
                    longitud ++; // Se aumenta la longitud en 1 por que 7D no esta es parte de la trama
                    flag = true ; // Se activa cuando se encuentra una secuencia de escape
                    suma -= 0x7D ; // Se le resta el byte que identifica el escape 7D
                }
                sub_trama = sub_trama + byte; // Se encadena el byte a las subtramas 
                suma += stoi(byte, nullptr, 16); // Se lleva a cabo una suma de el byte para verificar el checksum pasando el caracter a base 10
                j += 2; // j es el contador de la trama hasta la longitud
            }

            string byte_checksum = tramas.substr(i + longitud * 2 + 6,2); // Un ves terminadado de recorer la trama se extrae el checksum 
            tramas_totales ++ ; // Se aumenta la cantidad de tramas que se encontro 

            if (tramas.substr(i+ 8 + sub_trama.length() ,2)!="7E" or sub_trama.length() != longitud*2 ) {
                /* Verifica si la longitud de la trama no coincide 
                SI tramas.substr(i+ 8 + sub_trama.length() ,2)!="7E" da falso la trama es mas largo 
                SI sub_trama.length() != longitud*2 da falso la trama es mas corto
                */ 
                byte_checksum = ""; // Si no es la longitud correcta el checksum estara mal por lo que eatara vacio
                tramas_longitud_incorrecta ++ ; // Se lleva a cabo un acuenta de longitudes incorectas 
                cout << byte_bandera << byte_longitud << sub_trama << " Trama: Longitud Incorrecto "<<endl; 
                if (byte_checksum == "7E"){
                        string byte_escape = tramas.substr(j-2,2);
                        if (byte_escape == "7D"){
                            flag = true; // En caso de que el checksum sea 7E entonces entonces se encontro una secuencia de escape 
                            tramas_secuencia_escape ++ ; // Se aumenta la secuencia de escape
                        } else { 
                            escape = true; // En caso de no encontrar 7D
                            //i-=2; // 7E puede ser el inicio de una trama
                            byte_checksum = ""; // Si no es la longitud correcta el checksum estara mal por lo que eatara vacio
                        }
                }
            } else {
                int checksum = stoi(byte_checksum, nullptr, 16); // Convierte el checksum pasando el caracter a base 10
                tramas_longitud_correcta++ ;
                suma &= 0xFF ;
                suma = 0xFF - suma;
                if (checksum == suma ){
                    tramas_checksum_correcto ++ ; // Leva a cabo una cuenta de los checksum corectos
                    //cout << byte_bandera << byte_longitud << trama << byte_checksum << " Trama: Cheksum Correcto " << endl;
                } else {
                    tramas_checksum_incorrecto ++; // Cuenta las tramas con checsum incorecto
                    cout << byte_bandera << byte_longitud << sub_trama << byte_checksum << " Trama: Cheksum Incorrecto "<< endl ;
                }
                if (flag == true ){
                    cout << byte_bandera << byte_longitud << sub_trama << byte_checksum << " Trama: Secuencia con escape " << endl;
                }
            }   
            i +=(  byte_bandera.length() + byte_longitud.length() + sub_trama.length() + byte_checksum.length() );
        } else {
            cout <<"/ byte SALTADO:" << tramas.substr(i,2)<< endl;
            i += 2 ;
        }
    }

    cout << "Número total de tramas recibidas: " << tramas_totales << endl;
    cout << "Número de tramas con longitud correcta: " << tramas_longitud_correcta << endl;
    cout << "Número de tramas con longitud incorrecta: " << tramas_longitud_incorrecta << endl;
    cout << "Número de tramas con cheksum correcta: " << tramas_checksum_correcto << endl;
    cout << "Número de tramas con cheksum incorrecta: " << tramas_checksum_incorrecto << endl;
    cout << "Número de tramas que utilizan secuencia de escape: " << tramas_secuencia_escape << endl;
}

int main(){
    ifstream archivo;
    string tramas;
    
    archivo.open("Tramas_802-15-4.log",ios::in);
    if(archivo.fail()){
        cout<<"No se pudo abrir el archivo";
        exit(1);
    }    
    getline(archivo,tramas);    
    analizar_tramas(tramas);
    archivo.close();
    return 0;
}