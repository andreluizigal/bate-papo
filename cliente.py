import socket, pickle, threading, time
from mensagem import Mensagem

entrada = " "
usuario = " "

def main():
    HOST = 'localhost'
    PORT = 1900

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    global entrada

    primeira_vez = True

    while True:
        if entrada != "/ENTRAR":
            while entrada != "/ENTRAR":
                entrada = input("Digite /ENTRAR para entrar no chat: ")
                if entrada != "/ENTRAR": print("Comando invalido")

            usuario = input("Digite seu usuario: ")

            mensagem_entrada = Mensagem("/ENTRAR", usuario, "")
            dados_mensagem_entrada = pickle.dumps(mensagem_entrada)

            cliente.sendall(dados_mensagem_entrada)

            if primeira_vez:
                dados_mensagem = cliente.recv(4096)
                mensagem = pickle.loads(dados_mensagem)
                print(mensagem.texto)
                primeira_vez = False

        else:
            recebimento = threading.Thread(target=receberMensagem, args=[cliente, usuario])
            recebimento.start()
            enviarMensagem(cliente, usuario)
           

def receberMensagem(cliente, usuario):
    while True:
        data = cliente.recv(4096)
        
        mensagem = pickle.loads(data)
        if mensagem.tipo == "/ENTRAR":
            if mensagem.usuario == usuario: print(mensagem.texto)
            else: print(mensagem.usuario, "entrou!")

        elif mensagem.tipo == "/USUARIOS":
            print("Usuarios conectados: ")
            for u in mensagem.texto: print(u)
        
        elif mensagem.tipo == "/SAIR":
            if mensagem.usuario == usuario:
                print("Voce saiu...")
                global entrada
                entrada = " "
            else:
                print(mensagem.usuario, "saiu...")
        
        else:
            print(mensagem.usuario, ":", mensagem.texto)


def enviarMensagem(cliente, usuario):
    while True:
        global entrada
        if entrada != "/ENTRAR": break
        texto_mensagem = input()

        if texto_mensagem == "/USUARIOS":
            mensagem = Mensagem("/USUARIOS", usuario, "")
            dados_mensagem = pickle.dumps(mensagem)
            cliente.sendall(dados_mensagem)
        
        elif texto_mensagem == "/SAIR":
            mensagem = Mensagem("/SAIR", usuario, "")
            dados_mensagem = pickle.dumps(mensagem)
            cliente.sendall(dados_mensagem)
            entrada = " "

        
        else:
            mensagem = Mensagem("/NORMAL", usuario, texto_mensagem)
            dados_mensagem = pickle.dumps(mensagem)
            cliente.sendall(dados_mensagem)


main()