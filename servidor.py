import socket, pickle, threading
from mensagem import Mensagem

global usuarios, clientes
usuarios = []
clientes = []

def main():

    HOST = 'localhost'
    PORT = 1900
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        servidor.bind((HOST, PORT))
        servidor.listen(10)
        print("Servidor online escutando na porta:", PORT)
    except:
        return print('\nNão foi possível iniciar o servidor\n')

    while True:
        cliente, endereco = servidor.accept()

        thread = threading.Thread(target=receberMensagem, args=[cliente])
        thread.start()


def receberMensagem(cliente):
        
    while True:
        try:
            data = cliente.recv(4096)
            mensagem = pickle.loads(data)
            print("Mensagem: ", mensagem.tipo, mensagem.usuario, mensagem.texto)
        except:
            deletarCliente(cliente, mensagem.usuario)
            retorno = Mensagem("/SAIR", mensagem.usuario, mensagem.usuario + "saiu...")
            data_string = pickle.dumps(retorno)
            broadcast(data_string, cliente)

        if mensagem.tipo == "/ENTRAR":
            clientes.append(cliente)
            usuarios.append(mensagem.usuario)
            retorno = Mensagem("/ENTRAR", mensagem.usuario, "Conectado! Digite mensagens ou comandos:")
            data_string = pickle.dumps(retorno)
            cliente.sendall(data_string)
            broadcast(data_string, cliente)
        
        elif mensagem.tipo == "/USUARIOS":
            retorno = Mensagem("/USUARIOS", mensagem.usuario, usuarios) 
            data_string = pickle.dumps(retorno)
            cliente.sendall(data_string)
        
        elif mensagem.tipo == "/SAIR":
            deletarCliente(cliente, mensagem.usuario)
            retorno = Mensagem("/SAIR", mensagem.usuario, "")
            data_string = pickle.dumps(retorno)
            cliente.sendall(data_string)
            
            retorno.texto = mensagem.usuario + " saiu..."
            data_string = pickle.dumps(retorno)
            broadcast(data_string, cliente)
        
        else:
            broadcast(data, cliente)
            


def deletarCliente(cliente, usuario):
    clientes.remove(cliente)
    usuarios.remove(usuario)

def broadcast(data, cliente):
    for c in clientes:
        if c != cliente:
            try:
                c.sendall(data)

            except:
                deletarCliente(cliente)

main()