import streamlit as st
import pandas as pd
from pycaret.classification import *
from io import BytesIO
import xlsxwriter

@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def main():
    st.set_page_config(page_title='Credit-Scoring',
                      layout='wide',
                      initial_sidebar_state='expanded')
    
    st.title('Projeto EBAC - Credit Scoring')
    
    model = load_model(r'.\models\Final GBM Model 26Jun2025')
    
    tab1, tab2 = st.tabs(['Upload', 'Simulador'])
    
    with tab1:
        
        st.markdown('Para carregar os dados, os formatos devem atender aos requisitos abaixo:')
        st.markdown(unsafe_allow_html=True, body="""
        | Variável              | Formato | Valores                                                                               |
        |:----------------------|:--------|:--------------------------------------------------------------------------------------|
        | sexo                  | object  | • F <br>• M                                                                           |
        | posse_de_veiculo      | object  | • N <br>• S                                                                           |
        | posse_de_imovel       | object  | • S <br>• N                                                                           |
        | qtd_filhos            | int64   | • Mínimo: 0 <br>• Máximo: 14                                                          |
        | tipo_renda            | object  | • Pensionista <br>• Assalariado <br>• Empresário <br>• Servidor público <br>• Bolsista|
        | educacao              | object  | • Médio <br>• Superior completo <br>• Superior incompleto <br>• Fundamental <br>• Pós graduação |
        | estado_civil          | object  | • Casado <br>• Solteiro <br>• Viúvo <br>• União <br>• Separado                        |
        | idade                 | int64   | • Mínimo: 22 <br>• Máximo: 68                                                         |
        | tempo_emprego         | float64 | • Mínimo: 0 <br>• Máximo: 43                                                          |
        | qt_pessoas_residencia | float64 | • Mínimo: 1 <br>• Máximo: 15                                                          |
        | renda                 | float64 | • Mínimo: 100 <br>• Máximo: 42.000,00                                              |
        | cat_residencia        | object  | • Casa <br>• Com os pais <br>• Aluguel <br>• Comunitário <br>• Governamental <br>• Estúdio' |
        """)
    
        data_file = st.file_uploader("Bank marketing data", type = ['ftr'])
        
        pi = 36643 / (563357 + 36643)
    
        if (data_file is not None):
            df = pd.read_feather(data_file)
            
            prediction = predict_model(model, data=df)
            
            # ajuste para prevalência real
            prediction['Score_real'] = (
                (prediction['prediction_score'] * pi) /
                (prediction['prediction_score'] * pi +
                (1 - prediction['prediction_score']) * (1 - pi))
            )
            
            # gerar Excel
            df_xlsx = to_excel(prediction)
            
            # botão de download
            st.download_button(
                label='📥 Download',
                data=df_xlsx,
                file_name='Credit_score_.xlsx'
            )

    with tab2:
        with st.form('input_form'):
            st.subheader('Preencha os dados do cliente')
            
            # Primeira Linha
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                sexo = st.selectbox('Sexo', ['F', 'M'])
            with col2:
                posse_de_veiculo = st.selectbox('Posse de veículo', ['S', 'N'])
            with col3:
                posse_de_imovel = st.selectbox('Posse de imóvel', ['S', 'N'])
            with col4:
                qtde_filhos = st.slider('Quantidade de filhos', min_value=0, max_value=14, step=1)
            
            # Segunda Linha
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                tipo_renda = st.selectbox(
                    'Tipo de renda',
                    ['Pensionista', 'Assalariado', 'Empresário',
                     'Servidor público', 'Bolsista'])
            with col2:
                educacao = st.selectbox(
                    'Educação',
                    ['Médio', 'Fundamental', 'Superior Incompleto',
                     'Superior Completo', 'Pós graduação'])
            with col3:
                estado_civil = st.selectbox('Estado Civil',
                                            ['Casado', 'Solteiro', 'Viúvo', 'União', 'Separado'])
            with col4:
                idade = st.slider('Idade', min_value=22, max_value=68, step=1)
            
            # Terceira Linha
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                tempo_emprego = st.slider(
                    'Tempo de Emprego em Anos',
                    min_value=0.0, max_value=40.0, step=0.1)
            with col2:
                qt_pessoas_residencia = st.slider(
                    'Quantidade de Pessoas na Residência',
                    min_value=1, max_value=15, step=1)
            with col3:
                renda = st.number_input(
                    'Renda',
                    min_value=100, max_value=42000, step=100)
            with col4:
                cat_residencia = st.selectbox(
                    'Categoria de Residência',
                    ['Casa', 'Com os pais', 'Aluguel', 'Comunitário', 'Governamental', 'Estúdio'])
            
            submitted = st.form_submit_button('Calcular Score')
        
        if submitted:
            input_dict = {
                'sexo': [sexo],
                'posse_de_veiculo': [posse_de_veiculo],
                'posse_de_imovel': [posse_de_imovel],
                'qtd_filhos': [qtde_filhos],
                'tipo_renda': [tipo_renda],
                'educacao': [educacao],
                'estado_civil': [estado_civil],
                'idade': [idade],
                'tempo_emprego': [tempo_emprego],
                'qt_pessoas_residencia': [qt_pessoas_residencia],
                'renda': [renda],
                'cat_residencia': [cat_residencia]
            }
            
            df_input = pd.DataFrame(input_dict)
            
            input_predict = predict_model(model, data=df_input)
            
            input_predict['Score_real'] = (
                (input_predict['prediction_score'] * pi) /
                (input_predict['prediction_score'] * pi +
                (1 - input_predict['prediction_score']) * (1 - pi))
            )
            score = input_predict['Score_real'].iloc[0]
            st.info(f'Score do cliente: {score:.2%}')



if __name__ == '__main__':
	main()