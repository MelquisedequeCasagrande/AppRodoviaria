import sqlite3

class passagens:
    def __init__(self, idPassagem, CPF,Local_de_Embarque, Local_de_Desembarque, tempo_de_viagem, preço, poltrona):
        self.idPassagem               = idPassagem
        self.CPF                      = CPF
        self.Local_de_Embarque        = Local_de_Embarque
        self.Local_de_Desembarque     = Local_de_Desembarque
        self.tempo_de_viagem          = tempo_de_viagem
        self.preço                    = preço
        self.poltrona                 = poltrona

    
class Pessoas:
    def __init__(self,idPessoa,nome, CPF,telefone,email):
        self.idPessoa     = idPessoa
        self.nome         = nome
        self.telefone     = telefone
        self.email        = email
        self.CPF          = CPF
        
class VeiculoMotorizado:
    def __init__(self, idVeiculo, marca, cor, tipo, desembarque):
        self.idVeiculo       = idVeiculo
        self.marca           = marca
        self.cor             = cor
        self.tipo            = tipo
        self.desembarque     = desembarque
        
class BancodeDados_OnibusMelquisedequeCasagrande:
    def cadastrarPessoas(self, pessoas):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO pessoas(idPessoa, nome, CPF, telefone,email)
                       VALUES (?,?,?,?,?)
                       """,
                       (pessoas.idPessoa,pessoas.nome,pessoas.CPF,pessoas.telefone,pessoas.email)
                )
        conn.commit()
        conn.close()

    def CadastrarVendaDePassagem(self, passagem):
        conn  = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO passagens(idPassagem, CPF,Local_de_Embarque, Local_de_Desembarque, tempo_de_viagem, poltrona, preço)
                       VALUES (?,?,?,?,?,?,?)
                       """,
                       (passagem.idPassagem, passagem.CPF,passagem.Local_de_Embarque, passagem.Local_de_Desembarque, passagem.tempo_de_viagem, passagem.poltrona, passagem.preço)
                )        
        conn.commit()
        conn.close()
    
    def BuscarCPF(self, id):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT *
                        FROM pessoas
                        WHERE CPF = ?""",(str(id),)
                    )
        registro = cursor.fetchone()
        conn.close()
        if registro != None:
            return Pessoas(registro[0],registro[1],registro[2],registro[3], registro[4])
        else:
            return None

    def CadastrarVeiculo(self, veiculo):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO veiculos(idVeiculo, marca, cor, tipo, desembarque)
                       VALUES (?,?,?,?,?)
                       """,
                       (veiculo.idVeiculo, veiculo.marca, veiculo.cor, veiculo.tipo, veiculo.desembarque)
                )        
        conn.commit()
        conn.close()
        
        
    def listarPessoasPorId(self,id):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT * 
                        FROM pessoas
                        WHERE idPessoa = ?""",(str(id),)
                    )
        registropessoa = cursor.fetchone()
        conn.close()
        if registropessoa != None:
            return Pessoas(registropessoa[0], registropessoa[2], registropessoa[1], registropessoa[3], registropessoa[4])
        else:
            return None
        
    def ListarVeiculosCadastrados(self, id):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT * 
                        FROM veiculos
                        WHERE idVeiculo = ?""", (str(id),)
                  )
        registroveiculo = cursor.fetchone()
        conn.close()
        if registroveiculo != None:
            return VeiculoMotorizado(registroveiculo[0], registroveiculo[1], registroveiculo[2], registroveiculo[3], registroveiculo[4])
        else:
            return None
        
        
    def excluirVeiculo(self,veiculos):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                       DELETE 
                       FROM veiculos 
                       WHERE idVeiculo = ?""",(str(veiculos.idVeiculo),)
                       )
        conn.commit()
        conn.close()
        
    def ListarPassagens(self, id):
        conn   = sqlite3.connect('BancodeDados_OnibusMelquisedequeCasagrande.db')
        cursor = conn.cursor()
        cursor.execute("""
                       select veiculos.idVeiculo, veiculos.tipo, veiculos.desembarque, passagens.CPF, passagens.poltrona, passagens.preço, passagens.tempo_de_viagem
                       from veiculos join passagens
                       on passagens.Local_de_desembarque = veiculos.desembarque
                       where idPassagem = ?""", (str(id))
                  )
        registropassagens = cursor.fetchone()
        conn.close()
        if registropassagens != None:
            return registropassagens[0], registropassagens[1], registropassagens[2], registropassagens[3], registropassagens[4],registropassagens[5],registropassagens[6]
        else:
            return None
        
        

        
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import Config
Config.set('graphics', 'multisamples', 0)

import os
os.environ ["KIVY_AUDIO"] ="sdl2"

from kivy.app                  import App
from kivy.uix.boxlayout        import BoxLayout
from kivy.core.window          import Window


class Principal(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.size = (400,500)
        self.limpar()
    
    def limpar(self):
        self.ids.txID.text     = ' '
        self.ids.txMarca.text = ' '
        self.ids.txCor.text    = ' '
        self.ids.txTipo.text   = ' '
        self.ids.txDesembarque.text  = ' '
        self.ids.mensagem.text = ' '
   
    def sair(self):
        App.get_running_app().stop()
    
    def CadastrarVeiculo(self):
        App.get_running_app().registro_atual = None
        db = BancodeDados_OnibusMelquisedequeCasagrande()
        if App.get_running_app().registro_atual == None:
            Veiculo = VeiculoMotorizado(None,self.ids.txMarca.text,self.ids.txCor.text,
                                        self.ids.txTipo.text,
                                        self.ids.txDesembarque.text)
            db.CadastrarVeiculo(Veiculo)
            self.ids.mensagem.text = '[b][color=#00BFFF]Veiculo CADASTRADO com SUCESSO !![/color][/b]'
        else:
            self.ids.mensagem.text = '[b][color=#FF3333]Veiculo NAO cadastrado !![/color][/b]'
    

    def excluir(self):
        db = BancodeDados_OnibusMelquisedequeCasagrande()
        veiculos = db.ListarVeiculosCadastrados(self.ids.txID.text)
        App.get_running_app().registro_atual = veiculos
        if App.get_running_app().registro_atual != None:
            self.ids.txMarca.text   = veiculos.marca
            self.ids.txCor.text   = veiculos.cor
            self.ids.txTipo.text  = veiculos.tipo
            self.ids.txDesembarque.text  = veiculos.desembarque

            db.excluirVeiculo(App.get_running_app().registro_atual)
            self.ids.mensagem.text = '[b][color=#00BFFF]Veiculo EXCLUIDO com SUCESSO !![/color][/b]'
        else:
            self.ids.mensagem.text = '[b][color=#FF3333]Veiculo NAO encontrado !![/color][/b]'
        
class MinhaAgendaApp(App):
    def build(self):
        self.registro_atual = None
        self.title = 'Cadastrar veiculo - v1.1'
        return Principal()

minha = MinhaAgendaApp()
minha.run()        