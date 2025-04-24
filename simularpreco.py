import unicodedata

# ----------------------------- DADOS FIXOS -----------------------------

# Lista de cidades com seus respectivos estados
cidades = {
    "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Cabo Frio", "Campos dos Goytacazes", "Duque de Caxias", "São Gonçalo", "Volta Redonda", 
                       "Angra dos Reis", "Macaé", "Nova Iguaçu", "Itaperuna", "Barra Mansa", "Santo Antônio de Pádua", "Petrópolis", "Itaboraí", 
                       "Teresópolis", "Resende", "Rio das Ostras", "Araruama", "Armação dos Búzios"],
    "São Paulo": ["São Paulo", "Campinas", "Santos", "Ribeirão Preto", "Sorocaba", "São Bernardo do Campo", "São Caetano do Sul", "Guarulhos",
                  "Osasco", "Mauá", "Diadema", "Jundiaí", "Piracicaba", "Bauru", "Indaiatuba", "Limeira", "Franca", "Taubaté", "Barueri", 
                  "São José dos Campos"],
    "Brasília": ["Brasília", "Taguatinga", "Ceilândia", "Samambaia", "Gama", "Águas Claras", "Planaltina", "Sobradinho", "Recanto das Emas",
                 "Cruzeiro", "Guará", "Núcleo Bandeirante", "Brazlândia", "Candangolândia", "São Sebastião", "Paranoá", "Vicente Pires", 
                 "Jardim Botânico", "Santa Maria", "Varjão"]
}

# Fatores de multiplicação para o preço base, dependendo da localização
localizacao_fatores = {
    "centro": 1.5,
    "zona sul": 1.3,
    "zona norte": 1.2,
    "zona leste": 1.1,
    "zona oeste": 1.0
}

# Preço base do m² em cada cidade (em reais)
precos_base = {
    "Rio de Janeiro": 2200,
    "São Paulo": 1800,
    "Brasília": 2500
}
preco_quartos = 10000  # Preço adicional por quarto (em reais)

# ----------------------------- FUNÇÕES AUXILIARES -----------------------------

def formatar_moeda(valor):
    """Formata o valor para o formato de moeda brasileiro (R$)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def remover_acentos(resposta):
    """Remove acentos e normaliza a resposta para facilitar comparações."""
    return unicodedata.normalize('NFKD', resposta).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

def encontrar_cidade_correspondente(cidade_usuario):
    """Busca a cidade mais próxima nas listas de cidades válidas."""
    cidade_normalizada = remover_acentos(cidade_usuario)
    for estado, lista_cidades in cidades.items():
        for cidade in lista_cidades:
            if cidade_normalizada == remover_acentos(cidade):
                return estado, cidade
    return None, None  # Retorna None se nenhuma cidade correspondente for encontrada

# ----------------------------- FUNÇÃO PRINCIPAL - OBTENDO DADOS -----------------------------

def obter_dados_do_usuario():
    """Coleta os dados do usuário e garante a validação das respostas."""
    print("\nBEM-VINDO À SIMULAÇÃO DE PREÇO DE IMÓVEIS!")
    print("\n")  # Espaço entre o título e a próxima linha de perguntas

    def obter_resposta_com_erro(pergunta, tipo='texto', valor_default=None):
        """Obtém a resposta do usuário e valida as entradas."""
        while True:
            resposta = remover_acentos(input(pergunta))
            if resposta == "" and valor_default is not None:
                return valor_default
            if tipo == 'int' and resposta.isdigit():
                return int(resposta)
            if tipo == 'float' and resposta.replace('.', '', 1).isdigit():
                return float(resposta)
            if tipo == 'texto' and resposta:
                return resposta
            print("Entrada inválida! Tente novamente.")

    # Coleta os dados do imóvel
    tamanho = obter_resposta_com_erro("Digite o tamanho do imóvel (em m²): ", tipo="float")
    localizacao = obter_resposta_com_erro("Digite a localização do imóvel (Centro, Zona Sul, Zona Norte, Zona Leste, Zona Oeste): ")

    # Valida a localização
    while localizacao not in localizacao_fatores:
        print("Localização inválida. Tente novamente.")
        localizacao = obter_resposta_com_erro("Digite a localização do imóvel (Centro, Zona Sul, Zona Norte, Zona Leste, Zona Oeste): ")

    quartos = obter_resposta_com_erro("Digite o número de quartos do imóvel: ", tipo="int")
    idade = obter_resposta_com_erro("Digite a idade do imóvel (em anos): ", tipo="int")

    cidade = obter_resposta_com_erro("Digite a cidade do imóvel: ")

    # Valida a cidade
    estado, cidade_correspondente = encontrar_cidade_correspondente(cidade)
    while cidade_correspondente is None:
        print("Cidade inválida. Por favor, insira uma cidade válida.")
        cidade = obter_resposta_com_erro("Digite a cidade do imóvel: ")
        estado, cidade_correspondente = encontrar_cidade_correspondente(cidade)

    bairro = input("Digite o bairro do imóvel: ").strip().capitalize()

    proximidade_transporte = input("O imóvel está perto de transporte público? (s/n): ").strip().lower()
    proximidade_escola = input("O imóvel está perto de uma escola? (s/n): ").strip().lower()
    proximidade_hospital = input("O imóvel está perto de um hospital? (s/n): ").strip().lower()

    return tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado, cidade_correspondente, bairro

# ----------------------------- FUNÇÃO PARA CALCULAR O PREÇO -----------------------------

def calcular_preco_imovel(tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado):
    """Calcula o preço total do imóvel considerando todos os fatores."""
    transporte_fator = 1.1 if proximidade_transporte == "s" else 1.0
    escola_fator = 1.1 if proximidade_escola == "s" else 1.0
    hospital_fator = 1.1 if proximidade_hospital == "s" else 1.0
    fator_idade = 1 - (idade * 0.01)

    preco_base = precos_base.get(estado, precos_base["São Paulo"])
    preco_localizacao = preco_base * localizacao_fatores.get(localizacao, 1)
    preco_total = preco_localizacao * tamanho
    preco_total += preco_quartos * quartos
    preco_total *= fator_idade
    preco_total *= transporte_fator
    preco_total *= escola_fator
    preco_total *= hospital_fator

    return preco_total, fator_idade, transporte_fator, escola_fator, hospital_fator

# ----------------------------- FUNÇÃO PARA EXIBIR O RESULTADO -----------------------------

def exibir_resultado(tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado, cidade, bairro, preco, fator_idade, transporte_fator, escola_fator, hospital_fator):
    """Exibe o resultado final da simulação de preço."""
    preco_base = precos_base.get(estado, precos_base["São Paulo"])

    print("\nResultado da simulação:")
    print("\n")  # Espaço antes de exibir os resultados
    print(f"Tamanho do imóvel: {tamanho} m²")
    print(f"Localização: {localizacao.capitalize()}")
    print(f"Número de quartos: {quartos}")
    print(f"Idade do imóvel: {idade} anos")
    print(f"Cidade: {cidade.capitalize()}")
    print(f"Bairro: {bairro.capitalize()}")

    transporte_texto = "Sim" if proximidade_transporte == "s" else "Não"
    escola_texto = "Sim" if proximidade_escola == "s" else "Não"
    hospital_texto = "Sim" if proximidade_hospital == "s" else "Não"

    print(f"Proximidade de transporte público: {transporte_texto}")
    print(f"Proximidade de escola: {escola_texto}")
    print(f"Proximidade de hospital: {hospital_texto}")

    print("\nCálculo do preço:")
    print("\n")  # Espaço antes de exibir o cálculo
    print(f"- Preço base por m²: {formatar_moeda(preco_base)}")
    print(f"- Fator de localização: {localizacao.capitalize()} ({localizacao_fatores.get(localizacao, 1)}x)")
    print(f"- Preço total baseado no tamanho: {formatar_moeda(preco)}")
    print(f"- Preço adicional por quarto: {formatar_moeda(quartos * preco_quartos)}")
    print(f"- Ajuste pela idade: {fator_idade:.2f} (desconto de {100*(1-fator_idade):.2f}% por ser {idade} anos velho)")
    print(f"- Ajuste pela proximidade de transporte: {transporte_fator}x")
    print(f"- Ajuste pela proximidade de escola: {escola_fator}x")
    print(f"- Ajuste pela proximidade de hospital: {hospital_fator}x")
    print(f"\nPreço final do imóvel: {formatar_moeda(preco)}")

    continuar = input("\nVocê quer continuar a simulação com novos dados? (s/n): ").lower()
    if continuar == "s":
        print("Reiniciando a simulação...")
        simular_precos_imoveis()
    else:
        print("Obrigado por usar a simulação! Até a próxima!")

# ----------------------------- FUNÇÃO PRINCIPAL -----------------------------

def simular_precos_imoveis():
    """Inicia o processo de simulação de preços de imóveis."""
    tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado, cidade, bairro = obter_dados_do_usuario()
    preco, fator_idade, transporte_fator, escola_fator, hospital_fator = calcular_preco_imovel(tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado)
    exibir_resultado(tamanho, localizacao, quartos, idade, proximidade_transporte, proximidade_escola, proximidade_hospital, estado, cidade, bairro, preco, fator_idade, transporte_fator, escola_fator, hospital_fator)

# ----------------------------- EXECUÇÃO DA SIMULAÇÃO -----------------------------
simular_precos_imoveis()