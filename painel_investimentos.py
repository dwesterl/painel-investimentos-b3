import streamlit as st
import pandas as pd
import requests
import yfinance as yf

# Configuração da Página
st.set_page_config(
    page_title="Painel Híbrido: Top 30 + Veredito do Assessor",
    page_icon="📈",
    layout="wide"
)

# Título Principal
st.title("🛡️ Painel de Decisão Híbrido: Top 30 (Brapi & Veredito Institucional)")
st.markdown("### Fundamentos cruzados com Gestão de Risco e Opinião do Assessor de Investimentos")

# Token da Brapi configurado
TOKEN_BRAPI = "9yJxJMj4N2XBrVUD26Muin"

# Base de Dados Enriquecida com Análise do Assessor (Prós, Contras e Veredito)
blue_chips_info = {
    "ITUB4": {
        "Forte": "Maior ROE do setor bancário, gestão impecável e resiliência em crises.",
        "Risco": "Inadimplência no varejo e concorrência com fintechs.",
        "Veredito": "🟢 Compra (Core) - Prêmio no P/L é justificado pela segurança e histórico de execução."
    },
    "BBSE3": {
        "Forte": "Modelo asset-light, geração de caixa livre altíssima e dividendos gordos.",
        "Risco": "Sinistralidade no seguro rural (clima) e correlação com a Selic em queda.",
        "Veredito": "🟢 Compra (Renda) - Ideal para carteira previdenciária; máquina de pagar dividendos."
    },
    "BPAC11": {
        "Forte": "Melhor banco de investimentos da AL, forte captação de wealth management.",
        "Risco": "Receitas voláteis dependentes de M&A e mercado de capitais aquecido.",
        "Veredito": "🟡 Manter/Aguardar - Excelente ativo, mas costuma negociar a múltiplos muito esticados."
    },
    "TAEE11": {
        "Forte": "Receita 100% regulada e reajustada pela inflação (IPCA/IGP-M).",
        "Risco": "Alavancagem alta e queda no Dividend Yield devido a novos leilões pesados.",
        "Veredito": "🟡 Aguardar Desconto - Ativo defensivo ótimo, mas a margem de segurança atual é estreita."
    },
    "EGIE3": {
        "Forte": "Maior geradora privada do país, portfólio diversificado e contratos de longo prazo.",
        "Risco": "Risco hidrológico (secas) e alocação de capital em grandes obras de transmissão.",
        "Veredito": "🟢 Compra (Defensiva) - Gestão premium que entrega valor independente do ciclo econômico."
    },
    "CPLE6": {
        "Forte": "Enorme potencial de corte de custos e eficiência pós-privatização.",
        "Risco": "Risco regulatório e necessidade de provar execução da nova gestão privada.",
        "Veredito": "🟢 Compra (Turnaround) - Assimetria clara se a empresa atingir a eficiência dos pares privados."
    },
    "EQTL3": {
        "Forte": "Maior compradora e recuperadora de ativos estressados de energia do Brasil.",
        "Risco": "Endividamento constante e risco de execução na integração da Sabesp e outros ativos.",
        "Veredito": "🟢 Compra (Crescimento) - O P/L parece alto, mas o lucro futuro cresce muito rápido."
    },
    "WEGE3": {
        "Forte": "Fosso econômico global, ROE estratosférico e exposição cambial (dólar).",
        "Risco": "Sempre precificada para a perfeição; qualquer desaceleração gera forte queda nas ações.",
        "Veredito": "🟡 Aguardar / Compras Fracionadas - A melhor empresa da B3, mas não aceita erros no preço de entrada."
    },
    "PSSA3": {
        "Forte": "Liderança absoluta em seguro auto e expansão acelerada em saúde e banco.",
        "Risco": "Inflação de autopeças impactando diretamente a sinistralidade.",
        "Veredito": "🟢 Compra (Valor) - Negocia a múltiplos atrativos frente ao seu domínio de mercado."
    },
    "VULC3": {
        "Forte": "Dona da Olympikus, forte barreira de marca nacional e margens controladas.",
        "Risco": "Dependência do consumo interno e renda familiar.",
        "Veredito": "🟢 Compra (Small/Mid) - ROE altíssimo e P/L descontado, entrega muito com pouco capital."
    },
    "POMO4": {
        "Forte": "Liderança nacional em ônibus, ciclo de renovação de frotas e programa Caminho da Escola.",
        "Risco": "Negócio extremamente cíclico e sensível a financiamentos pesados (Finame).",
        "Veredito": "🟡 Manter - O ciclo de alta já está no preço; cuidado com o topo do ciclo de lucros."
    },
    "PETR4": {
        "Forte": "Pré-sal possui um dos menores custos de extração (breakeven) do mundo; muito caixa.",
        "Risco": "Interferência política direta na alocação de capital e retenção de dividendos.",
        "Veredito": "🟡 Compra Tática (Risco Retorno) - P/L muito baixo compensa parte do risco político; foco no dividendo."
    },
    "VALE3": {
        "Forte": "Geração de caixa livre massiva e vantagem competitiva mineral global.",
        "Risco": "Colapso do mercado imobiliário chinês estrutural; passivos ambientais.",
        "Veredito": "🟢 Compra (Contrarian) - Papel extremamente descontado pelo pânico com a China; boa margem de segurança."
    },
    "VIVT3": {
        "Forte": "Geração de caixa resiliente, liderança no pós-pago e dividendos constantes.",
        "Risco": "Setor exige Capex bilionário perpétuo, limitando o crescimento do lucro líquido.",
        "Veredito": "🟢 Compra (Renda Fixa Turbinada) - Funciona como um bond (título) protegido contra a inflação."
    },
    "ENGI11": {
        "Forte": "Gestão de distribuição eficiente com crescimento forte do consumo em suas áreas.",
        "Risco": "Alavancagem financeira (dívida) alta frente às taxas de juros atuais.",
        "Veredito": "🟡 Aguardar - O endividamento pressiona o lucro no curto prazo com a Selic elevada."
    }
}

small_caps_info = {
    "TUPY3": {
        "Forte": "Multinacional brasileira sólida, receitas em dólar/euro e fosso tecnológico em fundição.",
        "Risco": "Transição energética (ameaça a motores a combustão pesados no longuíssimo prazo).",
        "Veredito": "🟢 Compra (Desconto) - Negocia muito abaixo do valor justo com forte geração de caixa."
    },
    "FRAS3": {
        "Forte": "Dominância em reposição de autopeças (freios), setor que sofre menos em crises.",
        "Risco": "Volatilidade no custo do aço e das resinas.",
        "Veredito": "🟢 Compra (Crescimento) - Boa alocação de capital com aquisições inteligentes."
    },
    "STBP3": {
        "Forte": "Monopólio natural geográfico (Porto de Santos) e renovação contratual longa.",
        "Risco": "Renegociações tarifárias e dependência do fluxo global de contêineres.",
        "Veredito": "🟡 Manter - Excelentes fundamentos, mas o mercado já precificou grande parte da melhora operacional."
    },
    "KEPL3": {
        "Forte": "Déficit colossal de armazenagem agrícola no Brasil garante demanda estrutural por décadas.",
        "Risco": "Financiamentos do Plano Safra dão o tom do curto prazo; anos de seca travam vendas.",
        "Veredito": "🟢 Compra (Agro) - A melhor tese derivada do agronegócio na bolsa brasileira hoje."
    },
    "TOTS3": {
        "Forte": "Receita recorrente e altíssimo custo de troca (switching cost) para os clientes do ERP.",
        "Risco": "P/L historicamente muito alto, sem espaço para decepções nos balanços.",
        "Veredito": "🟡 Aguardar - Excelente empresa, mas múltiplos não oferecem margem de segurança a Graham."
    },
    "DIRR3": {
        "Forte": "Execução impecável em habitação popular e altíssimo ROE no setor de construção.",
        "Risco": "Dependência absoluta das regras governamentais do Minha Casa Minha Vida.",
        "Veredito": "🟢 Compra (Qualidade) - Melhor execução do setor, caixa líquido e forte pagadora de dividendos."
    },
    "SHUL4": {
        "Forte": "Consolidadora no mercado de compressores e governança tradicional.",
        "Risco": "Baixa liquidez na bolsa e correlação com a indústria de base.",
        "Veredito": "🟡 Manter - Empresa sólida, mas sofre com o ciclo industrial interno fraco."
    },
    "LOGN3": {
        "Forte": "Tese de infraestrutura forte (cabotagem) para fugir do custo rodoviário brasileiro.",
        "Risco": "Setor de alto investimento (navios caros) e oscilação do preço do bunker (combustível).",
        "Veredito": "🟢 Compra (Oportunidade) - P/L baixo e ganhos de sinergia pós-compra pela MSC."
    },
    "CAML3": {
        "Forte": "Marcas líderes absolutas e demanda inelástica (pessoas não param de comprar arroz/feijão).",
        "Risco": "Margens muito estreitas; sofre quando a matéria-prima sobe rápido demais.",
        "Veredito": "🟡 Aguardar - Empresa muito madura; falta um gatilho claro de crescimento forte."
    },
    "ABCB4": {
        "Forte": "O banco mais conservador do Brasil; foca em crédito corporativo de alta qualidade.",
        "Risco": "Inadimplência de cauda grossa (se uma grande empresa der default, machuca o balanço).",
        "Veredito": "🟢 Compra (Renda Segura) - Desconto patrimonial histórico (P/VP) e DY consistente."
    },
    "EVEN3": {
        "Forte": "Estoque limpo, foco em alta renda (Melnick) e forte posição de caixa.",
        "Risco": "Alta sensibilidade à curva de juros (financiamento imobiliário caro trava vendas).",
        "Veredito": "🟡 Aguardar Ciclo - Ação atrativa, mas o setor sofre pesado com Selic estruturalmente alta."
    },
    "MTRE3": {
        "Forte": "Qualidade construtiva premium em São Paulo.",
        "Risco": "Alavancagem pontual gerada por excesso de lançamentos no passado recente.",
        "Veredito": "🟡 Alerta - Ficar de fora até provar que conseguirá girar o estoque sem corroer margens."
    },
    "ROMI3": {
        "Forte": "Dominância em máquinas pesadas, forte geração de caixa em ciclos de investimento.",
        "Risco": "O primeiro setor a parar em crises e o último a retomar; volatilidade violenta no balanço.",
        "Veredito": "🟡 Aguardar - Papel clássico de ciclo; só se compra quando o balanço está no fundo do poço."
    },
    "RECV3": {
        "Forte": "Revitaliza campos terrestres com altíssima eficiência e custo de elevação baixo.",
        "Risco": "Reserva de vida útil curta requer M&As constantes; exposição total ao Brent.",
        "Veredito": "🟢 Compra (Valor) - Forte desconto frente aos pares do setor de óleo e gás; alvo claro de M&A."
    },
    "CURY3": {
        "Forte": "Giro de estoque brutal (vende tudo no lançamento); ROE astronômico sem precisar de dívida.",
        "Risco": "Já precificada para o cenário perfeito, pouca margem para erros.",
        "Veredito": "🟢 Compra (Premium) - A máquina mais eficiente da construção civil brasileira hoje."
    }
}


# Função rigorosa de Candles (Corrigida e Integra)
def identificar_padrao_candle_rigoroso(df):
    if len(df) < 5:
        return "Sem padrão"

    o0, h0, l0, c0 = df['Open'].iloc[-1], df['High'].iloc[-1], df['Low'].iloc[-1], df['Close'].iloc[-1]
    o1, h1, l1, c1 = df['Open'].iloc[-2], df['High'].iloc[-2], df['Low'].iloc[-2], df['Close'].iloc[-2]

    corpo0 = abs(c0 - o0)
    corpo1 = abs(c1 - o1)
    amplitude0 = h0 - l0

    if amplitude0 == 0 or corpo0 < (amplitude0 * 0.25):
        return "Sem padrão"

    sombra_inferior = min(o0, c0) - l0
    sombra_superior = h0 - max(o0, c0)
    ma9 = df['Close'].rolling(window=9).mean().iloc[-1]

    if (sombra_inferior >= (2.5 * corpo0)) and (sombra_superior <= (0.2 * corpo0)) and (c0 < ma9):
        return "🟢 Martelo"
    if (c1 < o1) and (c0 > o0) and (corpo0 > 1.3 * corpo1) and (c0 >= o1) and (o0 <= c1):
        return "🟢 Engolfo Alta"
    if (c1 > o1) and (c0 < o0) and (corpo0 > 1.3 * corpo1) and (c0 <= o1) and (o0 >= c1):
        return "🔴 Engolfo Baixa"

    return "⚪ Neutro"


# Função central com Fallback Robusto
@st.cache_data(ttl=3600)
def carregar_painel_completo(dicionario_ativos):
    resultados = []

    for ticker, info in dicionario_ativos.items():
        try:
            pl_val, roe_val, dy_val = "N/D", "N/D", "N/D"

            # 1. Tentativa via Brapi
            url_brapi = f"https://brapi.dev/api/quote/{ticker}?token={TOKEN_BRAPI}&fundamental=true"
            res = requests.get(url_brapi)
            if res.status_code == 200:
                data = res.json().get('results', [])
                if data:
                    item = data[0]
                    pl_raw = item.get('priceEarnings') or item.get('p_l') or item.get('pe')
                    roe_raw = item.get('returnOnEquity') or item.get('roe')
                    dy_raw = item.get('dividendYield') or item.get('dy')

                    if pl_raw is not None:
                        pl_val = f"{float(pl_raw):.1f}"
                    if roe_raw is not None:
                        val = float(roe_raw)
                        roe_val = f"{val * 100:.1f}%" if val <= 1.5 else f"{val:.1f}%"
                    if dy_raw is not None:
                        val = float(dy_raw)
                        dy_val = f"{val * 100:.1f}%" if val <= 1.0 else f"{val:.1f}%"

            # 2. Busca Técnica via yfinance e fallback
            acao = yf.Ticker(ticker + ".SA")
            df_cotacao = acao.history(period="3mo", interval="1d")

            if df_cotacao.empty:
                continue

            preco_atual = round(float(df_cotacao['Close'].iloc[-1]), 2)
            padrao = identificar_padrao_candle_rigoroso(df_cotacao)

            if len(df_cotacao) >= 21:
                ma21 = df_cotacao['Close'].rolling(window=21).mean().iloc[-1]
                tendencia = "Tendência de Alta" if preco_atual > ma21 else "Correção / Baixa"
            else:
                tendencia = "Neutro"

            # 3. Fallback inteligente via yfinance .info
            if pl_val == "N/D" or roe_val == "N/D" or dy_val == "N/D":
                try:
                    inf = acao.info
                    if pl_val == "N/D" and inf.get('trailingPE'):
                        pl_val = f"{float(inf.get('trailingPE')):.1f}"
                    if roe_val == "N/D" and inf.get('returnOnEquity'):
                        roe_val = f"{float(inf.get('returnOnEquity')) * 100:.1f}%"
                    if dy_val == "N/D" and inf.get('dividendYield'):
                        dy_f = float(inf.get('dividendYield'))
                        dy_val = f"{dy_f * 100:.1f}%" if dy_f <= 0.30 else f"{dy_f:.1f}%"
                except:
                    pass

            resultados.append({
                "Ticker": ticker,
                "Preço (R$)": preco_atual,
                "P/L": pl_val,
                "ROE": roe_val,
                "Div. Yield": dy_val,
                "🟢 Ponto Forte": info["Forte"],
                "⚠️ Alerta de Risco": info["Risco"],
                "🎯 Veredito do Assessor": info["Veredito"],
                "Candle": padrao,
                "Tendência": tendencia
            })
        except Exception as e:
            continue

    return pd.DataFrame(resultados)


# Abas no Streamlit
aba1, aba2 = st.tabs(["💎 Blue Chips (Tese & Veredito)", "🚀 Small Caps (Tese & Veredito)"])

with aba1:
    st.subheader("Top 15 Blue Chips - Opinião do Assessor e Fundamentos")
    st.markdown("Cruzamento de múltiplos financeiros com a vantagem competitiva e a tese de investimento.")
    with st.spinner("Analisando as Blue Chips..."):
        df_b = carregar_painel_completo(blue_chips_info)
        if not df_b.empty:
            st.dataframe(df_b, use_container_width=True)

with aba2:
    st.subheader("Top 15 Small Caps - Opinião do Assessor e Fundamentos")
    st.markdown("Identificação de valor oculto, riscos estruturais e recomendação estratégica.")
    with st.spinner("Analisando as Small Caps..."):
        df_s = carregar_painel_completo(small_caps_info)
        if not df_s.empty:
            st.dataframe(df_s, use_container_width=True)

st.markdown("---")
st.caption("Aviso: As opiniões refletem uma visão técnica institucional fundamentada e não garantem retornos futuros.")