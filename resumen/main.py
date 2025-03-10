from load_excel import loadExcel

excel_name="RESUMEN_2023.xlsx"

if __name__ == '__main__':
    df = loadExcel.loadEUInicial(excel_name)
    print(df)