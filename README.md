# Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento

## 1. Explicação do Funcionamento

Este projeto é um protótipo de software de **automação digital** desenvolvido em Python para auxiliar uma empresa industrial no controle de produção e qualidade de peças, substituindo a inspeção manual.

O sistema utiliza a **Programação Orientada a Objetos (POO)** para modelar as entidades (`Peca` e `GestaoProducao`), garantindo modularidade e fácil expansão.

### Fluxo de Trabalho Automatizado

1.  **Entrada de Dados:** O usuário (ou, em um cenário real, um sensor) fornece o `peso`, `cor` e `comprimento` da peça.
2.  **Avaliação de Qualidade:** A função interna `_avaliar_qualidade` aplica automaticamente os critérios de aprovação/reprovação com base em regras estritas.
    * **Aprovada:** Se todos os critérios forem atendidos.
    * **Reprovada:** Se um ou mais critérios falharem. O sistema registra o **motivo específico** da reprovação (Ex: "Peso fora do limite") para garantir a traçabilidade do defeito.
3.  **Armazenamento Logístico:** Peças **aprovadas** são direcionadas para a caixa em andamento.
4.  **Gestão de Caixas:** O sistema verifica se a capacidade máxima de **10 peças** foi atingida. Se estiver cheia, a caixa é automaticamente **fechada**, registrada no estoque final e uma nova caixa é iniciada.
5.  **Relatórios:** O sistema pode gerar relatórios consolidados sobre a performance da linha de produção (totais de aprovadas/reprovadas, e detalhamento dos motivos de falha).

---

## 2. Como Rodar o Programa (Passo a Passo)

### Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado em seu sistema.

### Execução

1.  **Baixe o Arquivo Python:**
    Salve o código fornecido como `digital_automation_challenge.py`.

2.  **Execute no Terminal:**
    Abra o terminal ou prompt de comando na pasta onde o arquivo foi salvo e execute:
    ```bash
    python digital_automation_challenge.py
    ```

3.  **Use o Menu Interativo:**
    O sistema iniciará exibindo um menu de opções. Digite o número da opção desejada e pressione `Enter`.

---

## 3. Exemplos de Entradas e Saídas

### Exemplo 1: Peça Aprovada (Cadastrando no Menu: Opção 1)

| Entrada do Usuário | Saída do Sistema (Parcial) |
| :--- | :--- |
| `peso (g): 100` | ✅ PEÇA CADASTRADA E AVALIADA |
| `cor: azul` | Status: APROVADA \| Motivo: Conforme |
| `comprimento (cm): 15` | [Armazenamento] Peça XXXX adicionada à Caixa 1. Capacidade: 1/10. |

### Exemplo 2: Peça Reprovada (Cadastrando no Menu: Opção 1)

| Entrada do Usuário | Saída do Sistema (Parcial) |
| :--- | :--- |
| `peso (g): 110` | ❌ PEÇA CADASTRADA E AVALIADA |
| `cor: vermelho` | Status: REPROVADA |
| `comprimento (cm): 12` | Motivo: Peso (110g) fora do limite \| Cor (Vermelho) não aprovada. |

### Exemplo 3: Fechamento de Caixa Automático

**(Resultado após a 10ª peça APROVADA ser cadastrada)**

| Evento | Saída do Sistema |
| :--- | :--- |
| Adição da 10ª Peça | 📦 CAIXA 1 FECHADA! (Total: 10 peças). 📦 Nova Caixa 2 iniciada. |
