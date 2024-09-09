import pandas as pd


def load_artists_data(artists_file):
    # Cargar el archivo artists_data.csv con los ids y nombres
    artists_df = pd.read_csv(artists_file)
    # Crear un diccionario {artistName: artistId} para búsquedas rápidas
    artist_dict = dict(zip(artists_df['name'], artists_df['id']))
    return artist_dict


def replace_artist_name_with_id(streaming_file, artist_dict, output_file):
    # Cargar el archivo streaming.csv
    streaming_df = pd.read_csv(streaming_file)

    # Filtrar solo las filas donde artistName está en artists_data.csv
    streaming_df['artistId'] = streaming_df['artistName'].map(artist_dict)

    # Eliminar las filas donde no se encontró un artistId (NaN)
    streaming_df = streaming_df.dropna(subset=['artistId'])

    # Eliminar la columna artistName y quedarnos con artistId
    streaming_df = streaming_df.drop(columns=['artistName'])

    # Guardar el nuevo CSV
    streaming_df.to_csv(output_file, index=False)
    print(f"El archivo ha sido guardado como {output_file}")


def main():
    # Cargar el archivo de artistas
    artists_file = "../../data/spotify/artists_data.csv"
    artist_dict = load_artists_data(artists_file)

    # Procesar el archivo de streaming
    streaming_file = "../../data/spotify/streaming.csv"
    output_file = "../../data/spotify/streaming_with_artist_id.csv"

    replace_artist_name_with_id(streaming_file, artist_dict, output_file)


if __name__ == "__main__":
    main()