import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd

df = pd.read_csv("data/2019_general_payments.csv")

app = dash.Dash(__name__)

server = app.server

PAGE_SIZE = 10

app.layout = html.Div([
    html.Div([
        html.Center([
            html.H1([
                "Better Open Payments Dashboard",
            ]),
        ]),
    ]),
    html.Div([
        html.Center([
            "Doctor Name Search",
            html.Br(),
            dcc.Input(
                id="datatable-search",
                type="text",
                placeholder="FirstName LastName",
            ),
        ])
    ]),
    html.Br(),
    dash_table.DataTable(
        id="datatable-paging",
        columns=[{"name":i, "id":i} for i in sorted(df.columns)],

        page_current=0,
        page_size=PAGE_SIZE,
        page_action="custom",

        sort_action="custom",
        sort_mode="single",
        sort_by=[],
    ),
    html.Div([
        dcc.Markdown("""
        ## What is Open Payments?

        Open Payments is a national disclosure program that promotes a more transparent and accountable health care system.

        Open Payments houses a publicly accessible database of payments that reporting entities, including drug and medical device companies, make to covered recipients like physicians.

        *Please note that CMS [Centers for Medicare & Medicaid Services] does not comment on what relationships may be beneficial or potential conflicts of interest.*
        *CMS publishes the data attested to by reporting entities.*
        *The data is open to individual interpretation.*

        Official Source: [https://www.cms.gov/openpayments](https://www.cms.gov/openpayments)
        """),
    ]),
    html.Div([
        dcc.Markdown("""
        ### Note:
        Dataset: Only contains 2019 General Payments.

        Github Repo: [wesleyacheng/open_payments_dashboard](https://github.com/wesleyacheng/open_payments_dashboard)

        Made with 🍵 by [@wesleyacheng](https://github.com/wesleyacheng)
        """)
    ]),
])


@app.callback(
    Output("datatable-paging", "data"),
    Input("datatable-paging", "page_current"),
    Input("datatable-paging", "page_size"),
    Input("datatable-paging", "sort_by"),
    Input("datatable-search", "value"),
)
def update_table(page_current, page_size, sort_by, search_str):
    #print(f"page_current: {page_current}, page_size:{page_size}, sort_by:{sort_by}, search_str:{search_str}")

    dff = df

    # filter dataset with user-inputted search string
    if search_str:
        dff = dff.loc[dff["DOCTOR_NAME"].str.contains(search_str.upper())]

    # sort by specific user-chosen configuration
    if sort_by:
        dff = dff.sort_values(
            sort_by[0]["column_id"],
            ascending=sort_by[0]["direction"] == "asc",
            inplace=False
        )

    # paginate
    dff = dff.iloc[page_current*page_size:(page_current+1)*page_size].to_dict("records")

    return dff

if __name__ == "__main__":
    app.run_server(debug=True)

