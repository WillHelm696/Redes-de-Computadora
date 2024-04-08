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
        bool flag = false; 
        bool escape = false;
        int suma = 0 ;
        string byte_bandera = tramas.substr(i,2);
        if (byte_bandera == "7E"){
            string sub_trama ;
            string byte_longitud = tramas.substr(i+2,4);
            int longitud = stoi(byte_longitud, nullptr, 16);
            int j = i+6;
            while ( j < ( i + 6 + longitud * 2 ) ){
                string byte = tramas.substr(j,2);
                if (byte == "7E"){
                    string byte_escape = tramas.substr(j-2,2);
                    if (byte_escape != "7D"){
                        escape = true;
                        i += 2;
                        break;
                    }
                    tramas_secuencia_escape ++ ;
                    longitud ++;
                    flag = true ;
                    suma -= 0x7D ;
                }
                sub_trama = sub_trama + byte;
                suma += stoi(byte, nullptr, 16);            
                j += 2;
            }

            string byte_checksum = tramas.substr(i + longitud * 2 + 6,2);
            int checksum = stoi(byte_checksum, nullptr, 16);
            tramas_totales ++ ;

            if (byte_checksum =="7E"){
                    string byte_escape = tramas.substr(j-2,2);
                    if (byte_escape != "7D"){
                        escape = true;
                        tramas_secuencia_escape ++ ;
                        i-=2;
                    }
            }
            if (tramas.substr(i+ 8 + sub_trama.length() ,2)!="7E" or sub_trama.length() != longitud*2 ) {
                byte_checksum = "";
                tramas_longitud_incorrecta ++ ;
                cout << byte_bandera << byte_longitud << sub_trama << " Trama: Longitud Incorrecto "<<endl;
                if (escape != true){
                    i +=2 ;
                }
            }  
            else {
                tramas_longitud_correcta++ ;
                suma &= 0xFF ;
                suma = 0xFF - suma;
                if (checksum == suma){
                    tramas_checksum_correcto ++ ;
                    //cout << byte_bandera << byte_longitud << trama << byte_checksum << " Trama: Cheksum Correcto " << endl;
                } else {
                    tramas_checksum_incorrecto ++;
                    cout << byte_bandera << byte_longitud << sub_trama << byte_checksum << " Trama: Cheksum Incorrecto "<< endl ;
                }
                if (flag == true ){
                    cout << byte_bandera << byte_longitud << sub_trama << byte_checksum << " Trama: Secuencia con escape " << endl;
                }
            }   
            i += 6 + sub_trama.length() + byte_checksum.length();
        } else {
            cout <<"/ byte SALTADO:" << tramas.substr(i-2,2)<< tramas.substr(i,2)<< tramas.substr(i,2)<< endl;
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