import yfinance as yf

def calcular_mayer(ticker):
    """Calcula o Múltiplo de Mayer para o ativo escolhido."""
    print(f"\n🔄 Buscando dados de {ticker}...\n")

    dados = yf.download(ticker, period="1y")

    if dados.empty:
        print("Não foi possível obter dados. Verifique o ticker ou conexão.")
        return None, None, None

    dados = dados.sort_index()

    dados["MM200"] = dados["Close"].rolling(window=200).mean()

    preco_atual = float(dados["Close"].iloc[-1])
    mm200 = float(dados["MM200"].iloc[-1])

    if mm200 == 0 or mm200 != mm200:  
        print("⚠️ Média móvel insuficiente (precisa de pelo menos 200 dias de dados).")
        return preco_atual, mm200, None

    mayer = preco_atual / mm200
    return preco_atual, mm200, mayer


def interpretar_mayer(mayer):
    """Dá uma leitura qualitativa do múltiplo."""
    if mayer < 1.0:
        return "🔵 Subvalorizado (abaixo da média de longo prazo)"
    elif mayer < 2.4:
        return "🟢 Faixa neutra"
    else:
        return "🔴 Supervalorizado (acima da média histórica)"


def main():
    print("\n")
    print("=" * 55)
    print("📈 ANALISADOR MÚLTIPLO DE MAYER - BITCOIN & IVVB11")
    print("=" * 55)

    print("\nEscolha o ativo:")
    print("1 - Bitcoin (BTC-USD)")
    print("2 - IVVB11 (ETF)")

    escolha = input("\nDigite o número da opção desejada: ").strip()

    if escolha == "1":
        ticker = "BTC-USD"
        nome = "Bitcoin"
    elif escolha == "2":
        ticker = "IVVB11.SA"
        nome = "IVVB11"
    else:
        print("❌ Opção inválida. Encerrando programa.")
        return

    preco, mm200, mayer = calcular_mayer(ticker)

    if preco is None:
        return

    print(f"\n📊 Resultado - {nome}")
    print("-" * 55)
    print(f"Preço atual: $ {preco:,.2f}")
    print(f"Média móvel 200 dias: $ {mm200:,.2f}")

    if mayer:
        print(f"Múltiplo de Mayer: {mayer:.2f}")
        print(f"Interpretação: {interpretar_mayer(mayer)}")
    else:
        print("Múltiplo de Mayer: não disponível (dados insuficientes)")

    print("-" * 55)


if __name__ == "__main__":
    main()
