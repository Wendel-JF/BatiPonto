from kivy.core.text import LabelBase


def register_fonts():
     # Roboto
    LabelBase.register(
        name="Roboto",
        fn_regular="fonts/Roboto/static/Roboto-Regular.ttf",
        fn_bold="fonts/Roboto/static/Roboto-Bold.ttf",
        fn_italic="fonts/Roboto/static/Roboto-Italic.ttf",
        fn_bolditalic="fonts/Roboto/static/Roboto-BoldItalic.ttf",
    )

    # Poppins
    LabelBase.register(
        name="Poppins",
        fn_regular="fonts/Poppins/Poppins-Regular.ttf",
        fn_bold="fonts/Poppins/Poppins-Bold.ttf",
        fn_italic="fonts/Poppins/Poppins-Italic.ttf",
        fn_bolditalic="fonts/Poppins/Poppins-BoldItalic.ttf",
    )

    # Montserrat
    LabelBase.register(
        name="Montserrat",
        fn_regular="fonts/Montserrat/static/Montserrat-Regular.ttf",
        fn_bold="fonts/Montserrat/static/Montserrat-Bold.ttf",
        fn_italic="fonts/Montserrat/static/Montserrat-Italic.ttf",
        fn_bolditalic="fonts/Montserrat/static/Montserrat-BoldItalic.ttf",
    )