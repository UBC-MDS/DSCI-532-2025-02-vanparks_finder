import dash_bootstrap_components as dbc

park_info_modal = dbc.Modal(
        id="park-info-modal",
        children=[
            dbc.ModalHeader("Selected Park Details"),
            dbc.ModalBody(id="park-info"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-park-modal", className="ml-auto", n_clicks=0)
            ),
        ],
        is_open=False,  
        size="lg", 
    )