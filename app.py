import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, chi2_contingency


# Загрузка датасета
def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except:
        return None


def main():
    st.set_page_config(page_title="Исследовательский проект", page_icon="📊", layout="wide",
                       initial_sidebar_state="expanded")
    uploaded_file = st.file_uploader('Загрузите csv файл', type=['csv'])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            st.write('Пример первых строк датасета')
            st.write(data.head())
            columns = data.columns
            col1, col2 = st.columns(2)

            with col1:
                selected_col1 = st.selectbox('Выберете переменную 1:', [""] + columns)
            with col2:
                selected_col2 = st.selectbox('Выберете переменную 2:', [""] + columns)

            if selected_col1 and selected_col2 and selected_col1 != selected_col2:
                col3, col4 = st.columns(2)
                with col3:
                    categorical_col1 = st.checkbox('Переменная 1 - категориальная', False)
                    if categorical_col1:
                        plt.figure(figsize=(8, 6))
                        data[selected_col1].value_counts().plot(kind='pie', autopct="%1.1f%%")
                        st.pyplot(plt.gcf())
                        plt.close()
                    else:
                        plt.figure(figsize=(10, 6))
                        sns.histplot(data[selected_col1], kde=True)
                        st.pyplot(plt.gcf())
                        plt.close()
                with col4:
                    categorical_col2 = st.checkbox('Переменная 2 - категориальная', False)
                    if categorical_col2:
                        plt.figure(figsize=(8, 6))
                        data[selected_col2].value_counts().plot(kind="pie", autopct="%1.1f%%")
                        st.pyplot(plt.gcf())
                        plt.close()
                    else:
                        plt.figure(figsize=(10, 6))
                        sns.histplot(data[selected_col2], kde=True)
                        st.pyplot(plt.gcf())
                        plt.close()
                st.write('## Выберите проверочный алгоритм:')
                st.write('''На данном этапе необходимо сформулировать две гипотезы H0 и H1:\n
    Под H0 (нулевая гипотеза) обычно принимается то, что переменные между которыми идет сравнение, никак не связанны между собой, а все совпадения случайны.\n
    Под H1 (альтернативная гипотеза) чаще всего подразумевается, что совпадения не случайны и различие между двумя переменными является значимыми.''')
                test_option = st.selectbox('', ['Нет', 'T-test', 'Mann-Whitney U-test', 'Chi-square test'])
                if test_option != 'Нет':
                    st.write('## Результат проверки:')
                    if test_option == 'Chi-square test' and (categorical_col1 or categorical_col2):
                        if categorical_col1 and categorical_col2:
                            contingency_table = pd.crosstab(data[selected_col1], data[selected_col2])
                            _, p_value, _, _ = chi2_contingency(contingency_table)
                            st.write(f'P-value: {p_value:.5f}')

                            if p_value < 0.05:
                                st.write('Различия статистически значимы')
                            else:
                                st.write('Различия не являются статистически значимыми')
                        else:
                            st.write('Выбранные переменные должны быть обе категориальными')
                    elif (test_option == 'T-test' or test_option == 'Mann-Whitney U-test') and not (
                            categorical_col1 or categorical_col2):
                        if test_option == 'T-test':
                            stat, p_value = ttest_ind(data[selected_col1], data[selected_col2])
                        else:
                            stat, p_value = mannwhitneyu(data[selected_col1], data[selected_col2])

                        st.write(f'Статистика теста: {stat}')
                        st.write(f'P-value: {p_value:.5f}')

                        if p_value < 0.05:
                            st.write('Различия статистически значимы')
                        else:
                            st.write('Различия не являются статистически значимыми')


if __name__ == '__main__':
    main()
