import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ.get("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = "2024!A2:I"


def main(objetos: list = []):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Primeiro, obter a última linha com dados
        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME
        ).execute()

        values = result.get('values', [])
        if not values:
            next_row = 1  # Planilha está vazia, começar na primeira linha
        else:
            next_row = len(values) + 1  # A próxima linha disponível

        # Dados para adicionar, usando o número da próxima linha disponível
        values = [
            # Substitua esses valores conforme necessário
            [next_row, objetos[0], objetos[1], objetos[2],
                objetos[3], objetos[4], objetos[5], objetos[6]]
        ]

        # Corpo da solicitação para append
        body = {
            'values': values
        }

        # Chamar a API para anexar os dados
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Valores adicionados: {
              result.get('updates').get('updatedCells')}")
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    # ["num_sei", "planilha", "frequencia", "descricao", "status", "categoria", "atendente" ]
    lista_sei = ["1400.01.0026993/2024-25", "", "",
                 "Concerto de repetidora portatil", "Concluído", "Telefonia", "Cap Cleyton"]
    main(lista_sei)
