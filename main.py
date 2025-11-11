def calcular_desconto(valor_compra, tipo_cliente, cupom):
    if valor_compra <= 0:                                #1
        return 0                                         #2

    if tipo_cliente == "premium":                        #3          
        desconto = 0.15                                  #4
    elif tipo_cliente == "regular":                      #5
        desconto = 0.05                                  #6
    else:                                                #7
        desconto = 0                                     #7                                     
    if cupom == "DESC10" and valor_compra > 100:         #8
        desconto += 0.10                                 #9

    valor_final = valor_compra * (1 - desconto)          #10

    if valor_final < 50:                                 #11
        valor_final += 5  # taxa mínima de entrega       #12

    return round(valor_final, 2)                         #13