from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import torch
import json
import pandas as pd

torch_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

assuntos =['Gerência de projetos',
 'Segurança da informação',
 'Redes de Computadores',
 'Gestão de TI',
 'Marketing',
 'Engenharia de requisitos',
 'Engenharia de software',
 "Linguagens de Programação de computadores",
 'Arquitetura e tecnologias de sistemas de informação',
 'Gestão de processos de negócio',
 'Banco de dados',
 ]
embedding_model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
tokenizer_kwargs = {'clean_up_tokenization_spaces':True}
model_kwargs = {'device': torch_device,'similarity_fn_name': 'cosine', 'tokenizer_kwargs': tokenizer_kwargs}
encode_kwargs = {'normalize_embeddings': True}

embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name,
                                   model_kwargs=model_kwargs, 
                                   encode_kwargs=encode_kwargs)

vectorstore = FAISS.from_texts(assuntos, embeddings)

#carregar arquivo json
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)
#calcular similaridade
questao = questions[0]
print(f"Questão: {questao}")

#checar o documento mais similar
topico_mais_similar = vectorstore.similarity_search_with_score(questao, 1)
#imprimir o tópico mais similar
print(f"O tópico mais similar é: {topico_mais_similar}")

similaridade = []
for question in questions:
    topico_mais_similar = vectorstore.similarity_search_with_score(question, 1)[0]
    print(f"Questão: {question}"[10:60])
    print(f"O tópico mais similar é: {topico_mais_similar[0]}, Score: {topico_mais_similar[1]}")    
    print("**"*30)
    similaridade.append(topico_mais_similar)

#criar dataframe
similaridade_p = [(score[0].page_content, score[1])  for  score  in similaridade]
df = pd.DataFrame(similaridade_p, columns=['Assunto', 'Score'])
df = df['Assunto'].value_counts().reset_index( name='Quantidade')

# grafico de barras
import matplotlib.pyplot as plt
import seaborn as sns
save_path = 'rank_assuntos.png'
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x='Assunto', y='Quantidade', data=df)
#quantidade de questões por tópico Na barra
for index, row in df.iterrows():
    plt.text(row.name, row.Quantidade, row.Quantidade, color='black', ha="center")
plt.title('Quantidade de questões por Assunto')
plt.xlabel('Assunto')
plt.ylabel('Quantidade')

plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(save_path)
