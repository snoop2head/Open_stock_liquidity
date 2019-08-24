import pygsheets
from app_pandas_to_dataframe_or_to_excel import get_table

def write_on_gs(firm_name):
    gc = pygsheets.authorize(service_file='credentials.json')

    df_data = get_table(firm_name)

    gs_url = 'input_your_project_google_spreadsheet_url'

    #open the google spreadsheet
    sh = gc.open_by_url(gs_url)

    #select the first sheet
    wks = sh[0]

    #update the first sheet with df, starting at cell B2.
    #updating overwrites the previous data
    wks.set_dataframe(df_data, 'B2')
    wks.update_value('A1', firm_name)
    return gs_url
