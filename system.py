import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Caminho para os ficheiros
data_dir = 'data/'
ratings_path = os.path.join(data_dir, 'ratings.csv')
movies_path = os.path.join(data_dir, 'movies.csv')
users_path = os.path.join(data_dir, 'users.csv')

# Carregar os dados
ratings = pd.read_csv(ratings_path)
movies = pd.read_csv(movies_path, encoding='utf-8')

# Criar DataFrame de utilizadores a partir do ficheiro ratings.csv
users_df = pd.DataFrame({'userId': ratings['userId'].unique()})
users_df['username'] = users_df['userId'].apply(lambda x: f"User{x}")  # Placeholder para nomes

if os.path.exists(users_path):
    users_df = pd.read_csv(users_path, encoding='utf-8-sig')
else:
    # Se não existir, cria uma estrutura inicial baseada no ratings.csv
    users_df = pd.DataFrame({'userId': ratings['userId'].unique()})
    users_df['username'] = users_df['userId'].apply(lambda x: f"User{x}")  # Placeholder

# Contar número de utilizadores únicos
num_users = users_df['userId'].max()  # Obtém o maior ID de utilizador existente

# Função para corrigir título dos filmes
def correct_movie_title(title):
    if title.endswith(', The'):
        title = 'The ' + title.replace(', The', '')
    elif title.endswith(', A'):
        title = 'A ' + title.replace(', A', '')
    return title

# Aplicar a correção ao título dos filmes
movies['title'] = movies['title'].apply(correct_movie_title)

# Função para login ou criação de conta
def user_login(users_df):
    username = input("Por favor, insira o seu nome de utilizador: ")

    if username in users_df['username'].values:
        print(f"Bem-vindo de volta, {username}!")
        user_id = users_df.loc[users_df['username'] == username, 'userId'].values[0]
    else:
        print("Novo utilizador! Vamos criar a sua conta.")
        user_id = num_users + 1  
        new_user = pd.DataFrame({'userId': [user_id], 'username': [username]})
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        print(f"Conta criada para {username}. Seu ID de utilizador é {user_id}.")
        users_df.to_csv(users_path, index=False, encoding='utf-8-sig')

    return user_id, users_df

# Função para obter avaliações iniciais com base em géneros
def get_genre_based_ratings(user_id, movies, ratings_df, genres=['Action', 'Drama', 'Comedy']):
    rated_movies = []
    
    for genre in genres:
        print(f"\nAvalie 5 filmes do género: {genre}")
        
        genre_df = movies[movies['genres'].str.contains(genre, case=False)].sample(frac=1).reset_index(drop=True)  # Embaralha os filmes
        count = 0
        index = 0

        while count < 5 and index < len(genre_df):
            movie = genre_df.iloc[index]
            rating = input(f"Filme: {movie['title']} (ID: {movie['movieId']}) - Nota (1 a 5, ou 0 para pular): ")

            if rating.isdigit():
                rating = int(rating)
                if rating > 0 and rating <= 5:
                    # Adiciona a avaliação apenas se o usuário der nota maior que 0
                    ratings_df = pd.concat([ratings_df, pd.DataFrame({
                        'userId': [user_id],
                        'movieId': [movie['movieId']],
                        'rating': [rating]
                    })], ignore_index=True)
                    rated_movies.append(movie['movieId'])
                    count += 1  # Conta apenas filmes realmente avaliados

            index += 1  # Passa para o próximo filme independentemente da resposta

    return ratings_df, rated_movies

# Função para recomendar filmes com base nas classificações do utilizador
def recommend_movies(user_id, user_similarity, user_movie_matrix, movies, top_n=3):
    user_similarities = user_similarity[user_id - 1]  # Ajusta para índice baseado em 0
    rated_movies = user_movie_matrix.loc[user_id]
    rated_movies = rated_movies[rated_movies > 0].index.tolist()

    movie_scores = {}
    similar_users = np.argsort(user_similarities)[::-1]  # Ordenar utilizadores pela semelhança

    for similar_user in similar_users:
        similar_user_ratings = user_movie_matrix.iloc[similar_user]
        for movie_id, rating in similar_user_ratings.items():
            if movie_id not in rated_movies and rating > 0:
                if movie_id not in movie_scores:
                    movie_scores[movie_id] = 0
                movie_scores[movie_id] += user_similarities[similar_user] * rating

    recommended_movie_ids = sorted(movie_scores, key=movie_scores.get, reverse=True)[:top_n]
    recommended_movie_titles = movies[movies['movieId'].isin(recommended_movie_ids)]['title'].tolist()

    return recommended_movie_titles

# Função para mostrar avaliações do utilizador
def show_user_ratings(user_id, ratings_df, movies):
    print(f"USER_ID: {user_id}")
    print("\nSuas avaliações:")
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    for _, row in user_ratings.iterrows():
        movie_title = movies[movies['movieId'] == row['movieId']]['title'].values[0]
        print(f"{movie_title}: {row['rating']}")

# Função principal de interação com o utilizador
def user_interaction(user_id, ratings_df, movies):
    while True:
        print("\nO que você deseja fazer?")
        print("1. Pedir recomendações")
        print("2. Ver minhas avaliações")
        print("3. Avaliar filmes")
        print("4. Sair")
        
        choice = input("Escolha uma opção (1/2/3/4): ")
        
        if choice == '1':
            
            ratings_df = ratings_df.groupby(['userId', 'movieId'], as_index=False).agg({'rating': 'mean'})

            user_movie_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)
            
            # Calcular similaridade de cosseno
            user_similarity = cosine_similarity(user_movie_matrix)
            
            recommendations = recommend_movies(user_id, user_similarity, user_movie_matrix, movies)
            print("\nTop 3 filmes recomendados:")
            for movie in recommendations:
                print(movie)
        
        elif choice == '2':
            show_user_ratings(user_id, ratings_df, movies)
        
        elif choice == '3':
            movie_name = input("Digite o nome do filme que deseja avaliar: ")
            movie = movies[movies['title'].str.contains(movie_name, case=False)]
            if not movie.empty:
                while True:  # Loop para garantir que a nota seja válida
                    rating = input(f"Filme encontrado: {movie.iloc[0]['title']} - Nota (1 a 5): ")

                    # Verifica se a nota é válida
                    if rating.isdigit() and int(rating) > 0 and int(rating) <= 5:
                        # Adicionar avaliação
                        new_rating = pd.DataFrame({
                            'userId': [user_id],
                            'movieId': [movie.iloc[0]['movieId']],
                            'rating': [int(rating)]
                        })
                        ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
                        print(f"Avaliação registrada para o filme: {movie.iloc[0]['title']}")
                        break  # Sai do loop após inserir a avaliação

                    else:
                        print("Nota inválida. Por favor, insira uma nota entre 1 e 5.")
            else:
                print("Filme não encontrado.")
        
        elif choice == '4':
            ratings_df.to_csv(ratings_path, index=False)
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução do sistema:
user_id, users_df = user_login(users_df)

# Se for um novo utilizador, pedir avaliações
if user_id > num_users:
    ratings, rated_movies = get_genre_based_ratings(user_id, movies, ratings)

# Interação contínua
user_interaction(user_id, ratings, movies)
