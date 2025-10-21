import uuid

# --- Classes de Gestão BY PAULO AUGUSTO SAMPAIO ---

class Peca:
    """Representa uma peça produzida com seus atributos e status de qualidade."""
    def __init__(self, peso, cor, comprimento):
        # ID único encurtado para rastreabilidade
        self.id = str(uuid.uuid4())[:8]  
        self.peso = peso
        self.cor = cor.lower()
        self.comprimento = comprimento
        self.status = "PENDENTE"
        self.motivo = ""

    def __str__(self):
        return (
            f"ID: {self.id} | Status: {self.status.ljust(10)} | "
            f"Peso: {self.peso}g | Cor: {self.cor.capitalize()} | "
            f"Comprimento: {self.comprimento}cm | Motivo: {self.motivo}"
        )

class GestaoProducao:
    """Gerencia todas as peças, o processo de qualidade e o armazenamento em caixas."""
    CAPACIDADE_CAIXA = 10

    def __init__(self):
        self.pecas_aprovadas = []
        self.pecas_reprovadas = []
        self.caixas_fechadas = []
        self.caixa_atual = []  # Peças na caixa que está em andamento
        self.total_pecas_produzidas = 0
        self.contador_caixas = 1

    def _avaliar_qualidade(self, peca):
        """Aplica os critérios de aprovação/reprovação."""
        motivos_reprovacao = []

        # 1. Critério de Peso (95g a 105g)
        if not (95 <= peca.peso <= 105):
            motivos_reprovacao.append(f"Peso ({peca.peso}g) fora do limite (95-105g)")

        # 2. Critério de Cor (azul ou verde)
        if peca.cor not in ['azul', 'verde']:
            motivos_reprovacao.append(f"Cor ({peca.cor.capitalize()}) não aprovada (esperado: azul/verde)")

        # 3. Critério de Comprimento (10cm a 20cm)
        if not (10 <= peca.comprimento <= 20):
            motivos_reprovacao.append(f"Comprimento ({peca.comprimento}cm) fora do limite (10-20cm)")

        if motivos_reprovacao:
            peca.status = "REPROVADA"
            peca.motivo = " | ".join(motivos_reprovacao)
            self.pecas_reprovadas.append(peca)
        else:
            peca.status = "APROVADA"
            peca.motivo = "Conforme"
            self.pecas_aprovadas.append(peca)
            self._armazenar_peca(peca)

    def _armazenar_peca(self, peca):
        """Armazena a peça aprovada e gerencia o fechamento das caixas."""
        self.caixa_atual.append(peca)
        print(f"\n[Armazenamento] Peça {peca.id} adicionada à Caixa {self.contador_caixas}. Capacidade: {len(self.caixa_atual)}/{self.CAPACIDADE_CAIXA}.")

        if len(self.caixa_atual) == self.CAPACIDADE_CAIXA:
            self._fechar_caixa()

    def _fechar_caixa(self):
        """Fecha a caixa atual e inicia uma nova."""
        caixa_fechada = {
            'id': self.contador_caixas,
            'total_pecas': len(self.caixa_atual),
            'pecas_ids': [p.id for p in self.caixa_atual]
        }
        self.caixas_fechadas.append(caixa_fechada)
        print(f"\n📦 CAIXA {self.contador_caixas} FECHADA! (Total: {len(self.caixa_atual)} peças).")
        
        # Inicia nova caixa
        self.caixa_atual = []
        self.contador_caixas += 1
        print(f"📦 Nova Caixa {self.contador_caixas} iniciada.")

    # --- Funções do Menu Interativo ---

    def cadastrar_peca(self):
        """Recebe dados da peça, avalia a qualidade e a armazena."""
        print("\n--- Cadastro de Nova Peça ---")
        try:
            # Entrada de dados
            peso = float(input("Digite o peso (g): "))
            cor = input("Digite a cor (Ex: azul, verde, vermelho): ")
            comprimento = float(input("Digite o comprimento (cm): "))

            if peso <= 0 or comprimento <= 0:
                raise ValueError("Peso e comprimento devem ser positivos.")

            nova_peca = Peca(peso, cor, comprimento)
            self.total_pecas_produzidas += 1
            
            # Avaliação automática
            self._avaliar_qualidade(nova_peca)
            
            print(f"\n✅ PEÇA CADASTRADA E AVALIADA:")
            print(nova_peca)

        except ValueError as e:
            print(f"\n❌ ERRO DE ENTRADA: Valor inválido. Verifique se o peso/comprimento são números válidos. Detalhe: {e}")

    def listar_pecas(self):
        """Lista todas as peças aprovadas e reprovadas."""
        print("\n--- Peças Aprovadas ---")
        if not self.pecas_aprovadas:
            print("Nenhuma peça aprovada ainda.")
        for peca in self.pecas_aprovadas:
            print(peca)
            
        print("\n--- Peças Reprovadas ---")
        if not self.pecas_reprovadas:
            print("Nenhuma peça reprovada ainda.")
        for peca in self.pecas_reprovadas:
            print(peca)

    def remover_peca(self):
        """Remove uma peça cadastrada (aprovada ou reprovada) pelo ID."""
        peca_id = input("Digite o ID da peça a ser removida (8 caracteres): ").strip()
        
        # Procura nas aprovadas
        for i, peca in enumerate(self.pecas_aprovadas):
            if peca.id == peca_id:
                del self.pecas_aprovadas[i]
                
                # Remove da caixa atual se estiver lá
                for j, p_caixa in enumerate(self.caixa_atual):
                    if p_caixa.id == peca_id:
                        del self.caixa_atual[j]
                        print(f"✅ Peça {peca_id} aprovada removida e retirada da Caixa {self.contador_caixas}.")
                        self.total_pecas_produzidas -= 1
                        return

                print(f"✅ Peça {peca_id} aprovada removida.")
                self.total_pecas_produzidas -= 1
                return

        # Procura nas reprovadas
        for i, peca in enumerate(self.pecas_reprovadas):
            if peca.id == peca_id:
                del self.pecas_reprovadas[i]
                print(f"✅ Peça {peca_id} reprovada removida.")
                self.total_pecas_produzidas -= 1
                return

        print(f"❌ Peça com ID {peca_id} não encontrada nas listas de Aprovadas ou Reprovadas.")

    def listar_caixas_fechadas(self):
        """Lista as caixas que já atingiram a capacidade e foram fechadas."""
        print("\n--- Caixas Fechadas ---")
        if not self.caixas_fechadas:
            print("Nenhuma caixa fechada ainda.")
            return

        for caixa in self.caixas_fechadas:
            print(f"📦 CAIXA ID: {caixa['id']} | Total de Peças: {caixa['total_pecas']} | IDs: {', '.join(caixa['pecas_ids'])}")
            
        print(f"\n📦 CAIXA ATUAL (EM ANDAMENTO) ID: {self.contador_caixas} | Peças: {len(self.caixa_atual)}/{self.CAPACIDADE_CAIXA}")
        if self.caixa_atual:
            print(f"IDs: {', '.join([p.id for p in self.caixa_atual])}")

    def gerar_relatorio_final(self):
        """Gera um relatório consolidado com os totais de produção e qualidade."""
        
        # Fechar caixa atual só se tiver peças e ainda não estiver vazia
        if self.caixa_atual:
            print("\nAVISO: Fechando a caixa atual para o relatório...")
            self._fechar_caixa()

        total_aprovadas = len(self.pecas_aprovadas)
        total_reprovadas = len(self.pecas_reprovadas)
        total_caixas_fechadas = len(self.caixas_fechadas)
        
        # Consolidação dos motivos de reprovação
        motivos_contagem = {}
        for peca in self.pecas_reprovadas:
            for motivo in peca.motivo.split(" | "):
                motivos_contagem[motivo] = motivos_contagem.get(motivo, 0) + 1
                
        print("\n=======================================================")
        print("                 RELATÓRIO DE PRODUÇÃO                 ")
        print("=======================================================")
        print(f"TOTAL DE PEÇAS PRODUZIDAS: {self.total_pecas_produzidas}")
        print("-------------------------------------------------------")
        print(f"✅ TOTAL DE PEÇAS APROVADAS: {total_aprovadas}")
        print(f"❌ TOTAL DE PEÇAS REPROVADAS: {total_reprovadas}")
        print(f"📦 QUANTIDADE DE CAIXAS UTILIZADAS: {total_caixas_fechadas}")
        print("-------------------------------------------------------")
        print("MOTIVOS DE REPROVAÇÃO CONSOLIDADOS:")
        if motivos_contagem:
            for motivo, contagem in motivos_contagem.items():
                print(f"- {motivo}: {contagem} ocorrência(s)")
        else:
            print("- Nenhuma reprovação registrada.")
        print("=======================================================\n")

# --- Função Principal e Menu ---

def main():
    """Inicializa o sistema de gestão e exibe o menu interativo."""
    gestao = GestaoProducao()
    
    while True:
        print("\n=============================================")
        print("  SISTEMA DE GESTÃO DE QUALIDADE - PROTÓTIPO ")
        print("=============================================")
        print("1. Cadastrar nova peça (Avaliação Automática)")
        print("2. Listar peças aprovadas/reprovadas")
        print("3. Remover peça cadastrada (ID)")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final e Sair")
        print("=============================================")
        
        escolha = input("Selecione uma opção: ").strip()
        
        if escolha == '1':
            gestao.cadastrar_peca()
        elif escolha == '2':
            gestao.listar_pecas()
        elif escolha == '3':
            gestao.remover_peca()
        elif escolha == '4':
            gestao.listar_caixas_fechadas()
        elif escolha == '5':
            gestao.gerar_relatorio_final()
            print("Sistema encerrado. Obrigado!")
            break
        else:
            print("\nOpção inválida. Por favor, escolha um número de 1 a 5.")

if __name__ == "__main__":
    main()
